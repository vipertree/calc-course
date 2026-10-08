"""Full-length practice exams: access, the server-side clock and part locking, grading, and the score report.
Uses the built exam (python3 build.py exam-ab1 --web)."""
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.utils import timezone

from accounts.models import Profile
from . import exams
from .models import ExamAttempt

SLUG = "ab1"


def make_user(name, full=False):
    u = User.objects.create_user(name, password="pw123456")
    Profile.objects.create(user=u, display_name=name.title(), full_access=full)
    return u


class ExamBase(TestCase):
    def setUp(self):
        self.pub, self.priv = exams.public(SLUG), exams.private(SLUG)
        self.assertIsNotNone(self.pub, "build the exam first: python3 build.py exam-ab1 --web")
        self.user = make_user("sam")
        self.c = Client()
        self.c.force_login(self.user)

    def start(self):
        r = self.c.post(f"/exams/{SLUG}/start/")
        self.assertEqual(r.status_code, 302)
        return ExamAttempt.objects.get(user=self.user, exam=SLUG, finished__isnull=True)

    def api(self, att, action, **body):
        return self.c.post(f"/api/exams/{SLUG}/{att.pk}/{action}/", data=json.dumps(body), content_type="application/json")

    def key(self, item):
        return self.priv["items"][item]["answer"]

    def items(self, k):
        return [it["id"] for it in self.pub["parts"][k]["items"]]

    def rewind(self, att, minutes):
        """Move the running part's start back in time, as if the student had been working that long."""
        att.refresh_from_db()
        att.part_started -= timedelta(minutes=minutes)
        att.save()
        return att.part_started


class Format(ExamBase):
    def test_the_exam_has_the_ap_layout(self):
        ps = self.pub["parts"]
        self.assertEqual([(p["key"], p["kind"], p["calc"], p["minutes"], len(p["items"])) for p in ps],
                         [("1A", "mcq", False, 60, 30), ("1B", "mcq", True, 45, 15), ("2A", "frq", True, 30, 2), ("2B", "frq", False, 60, 4)])
        self.assertEqual(self.pub["mc_total"], 45)
        self.assertEqual(self.pub["frq_total"], 54)
        self.assertAlmostEqual(self.pub["mc_weight"], 1.2)
        for q in self.pub["parts"][2]["items"] + self.pub["parts"][3]["items"]:
            self.assertEqual(sum(p["points"] for p in q["parts"]), 9)

    def test_answers_and_topics_stay_private(self):
        blob = json.dumps(self.pub)
        self.assertNotIn('"solution"', blob)
        self.assertNotIn('"answer"', blob)
        self.assertNotIn('"rubric"', blob)
        self.assertNotIn('"topic"', blob)

    def test_no_em_dashes_or_browser_dialogs(self):
        self.assertNotIn("—", json.dumps(exams.load(SLUG)))
        js = (Path(__file__).resolve().parent.parent / "static" / "js" / "exam.js").read_text()
        code = re.sub(r"/\*.*?\*/|//[^\n]*", "", js, flags=re.S)
        self.assertIsNone(re.search(r"\b(alert|confirm|prompt)\s*\(", code))


class Access(ExamBase):
    def test_free_exam_needs_only_an_account(self):
        anon = Client()
        r = anon.get(f"/exams/{SLUG}/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r["Location"])
        self.assertEqual(anon.post(f"/exams/{SLUG}/start/").status_code, 302)        # login_required
        self.assertFalse(ExamAttempt.objects.exists())
        r = self.c.get(f"/exams/{SLUG}/")                                               # sam has no membership
        self.assertContains(r, "Go to Section I, Part A")

    def test_members_only_flag_gates_the_exam(self):
        pub = dict(self.pub, members_only=True)
        self.assertFalse(exams.can_take(self.user, pub))
        self.assertTrue(exams.can_take(make_user("paid", full=True), pub))
        self.assertTrue(exams.can_take(self.user, dict(self.pub, members_only=False)))

    def test_members_only_exam_is_locked_end_to_end(self):
        orig = exams.public
        exams.public = lambda slug: dict(orig(slug), members_only=True) if orig(slug) else None
        try:
            r = self.c.get(f"/exams/{SLUG}/")
            self.assertContains(r, "are for members")
            self.assertEqual(self.c.post(f"/exams/{SLUG}/start/").status_code, 403)
            self.assertEqual(self.c.get(f"/exams/{SLUG}/print/exam/").status_code, 403)
            member = Client()
            member.force_login(make_user("paid", full=True))
            self.assertEqual(member.post(f"/exams/{SLUG}/start/").status_code, 302)
        finally:
            exams.public = orig

    def test_someone_elses_attempt_is_not_found(self):
        att = self.start()
        other = Client()
        other.force_login(make_user("lee"))
        self.assertEqual(other.get(f"/exams/{SLUG}/attempt/{att.pk}/").status_code, 404)
        self.assertEqual(other.post(f"/api/exams/{SLUG}/{att.pk}/begin/").status_code, 404)

    def test_start_resumes_the_sitting_in_progress(self):
        a = self.start()
        b = self.start()
        self.assertEqual(a.pk, b.pk)


class Clock(ExamBase):
    def test_page_holds_only_the_running_part(self):
        att = self.start()
        page = self.c.get(f"/exams/{SLUG}/attempt/{att.pk}/").content.decode()
        self.assertNotIn(self.items(0)[0], page)                 # not started: no questions at all
        self.api(att, "begin")
        page = self.c.get(f"/exams/{SLUG}/attempt/{att.pk}/").content.decode()
        self.assertIn(self.items(0)[0], page)
        for k in (1, 2, 3):                                       # no later part, so no peeking at the FRQs
            self.assertNotIn(f'"{self.items(k)[0]}"', page)
        self.assertNotIn('"solution"', page)
        self.assertNotIn('"answer"', page.replace('"answers"', ""))

    def test_reload_does_not_restart_the_clock(self):
        att = self.start()
        self.api(att, "begin")
        self.rewind(att, 20)
        r = self.api(att, "begin").json()
        self.assertTrue(r["state"]["running"])
        self.assertAlmostEqual(r["state"]["remaining"], 40 * 60, delta=5)

    def test_answers_save_while_the_part_runs(self):
        att = self.start()
        self.api(att, "begin")
        q = self.items(0)[0]
        self.assertTrue(self.api(att, "answer", item=q, value="C").json()["ok"])
        self.assertTrue(self.api(att, "answer", item=q, value="B").json()["ok"])
        att.refresh_from_db()
        self.assertEqual(att.answers, {q: "B"})
        self.assertEqual(self.api(att, "answer", item=q, value="E").status_code, 409)      # not a choice

    def test_no_answers_before_a_part_starts(self):
        att = self.start()
        r = self.api(att, "answer", item=self.items(0)[0], value="A")
        self.assertEqual(r.status_code, 409)

    def test_a_later_part_cannot_be_answered_early(self):
        att = self.start()
        self.api(att, "begin")
        self.assertEqual(self.api(att, "answer", item=self.items(1)[0], value="A").status_code, 409)

    def test_late_answer_is_refused_and_the_part_closes_at_its_deadline(self):
        att = self.start()
        self.api(att, "begin")
        q = self.items(0)[0]
        self.api(att, "answer", item=q, value="A")
        started = self.rewind(att, 61)                             # the client clock is not consulted at all
        r = self.api(att, "answer", item=q, value="B")
        self.assertEqual(r.status_code, 409)
        att.refresh_from_db()
        self.assertEqual(att.answers[q], "A")
        self.assertEqual(att.part, 1)
        self.assertIsNone(att.part_started)                        # Part B waits for its own Start
        self.assertTrue(att.timing["1A"]["timed_out"])
        end = datetime.fromisoformat(att.timing["1A"]["end"])
        self.assertEqual(end, started + timedelta(minutes=60))     # closed at the deadline, not when noticed

    def test_grace_covers_network_lag_only(self):
        att = self.start()
        self.api(att, "begin")
        q = self.items(0)[0]
        att.refresh_from_db()
        att.part_started -= timedelta(minutes=60, seconds=5)       # 5 s past the deadline: in flight when time ran out
        att.save()
        self.assertTrue(self.api(att, "answer", item=q, value="D").json()["ok"])

    def test_a_finished_part_cannot_be_reopened(self):
        att = self.start()
        self.api(att, "begin")
        q = self.items(0)[0]
        self.assertTrue(self.api(att, "submit", part="1A").json()["ok"])
        self.assertEqual(self.api(att, "answer", item=q, value="A").status_code, 409)
        self.assertEqual(self.api(att, "flag", item=q, on=True).status_code, 409)
        self.assertEqual(self.api(att, "submit", part="1A").status_code, 409)              # a stale tab can't end 1B
        self.api(att, "begin")
        att.refresh_from_db()
        self.assertEqual(att.part, 1)
        self.assertEqual(self.api(att, "answer", item=q, value="A").status_code, 409)

    def test_flags(self):
        att = self.start()
        self.api(att, "begin")
        q = self.items(0)[3]
        self.api(att, "flag", item=q, on=True)
        att.refresh_from_db()
        self.assertEqual(att.flags, [q])
        self.api(att, "flag", item=q, on=False)
        att.refresh_from_db()
        self.assertEqual(att.flags, [])

    def test_an_abandoned_sitting_runs_out_part_by_part(self):
        att = self.start()
        self.api(att, "begin")
        self.rewind(att, 24 * 60)                                  # gone a day: only the running part times out
        r = self.c.get(f"/exams/{SLUG}/")
        att.refresh_from_db()
        self.assertEqual(att.part, 1)
        self.assertIsNone(att.finished)
        self.assertContains(r, "You have an exam in progress")


class Scoring(ExamBase):
    def run_through(self, att, right=(), wrong=()):
        for k, p in enumerate(self.pub["parts"]):
            self.api(att, "begin")
            for iid in self.items(k):
                if iid in right:
                    self.api(att, "answer", item=iid, value=self.key(iid))
                elif iid in wrong:
                    self.api(att, "answer", item=iid, value=next(L for L in "ABCD" if L != self.key(iid)))
            self.api(att, "submit", part=p["key"])
        att.refresh_from_db()
        return att

    def test_multiple_choice_is_graded_at_the_end(self):
        att = self.start()
        mc = self.items(0) + self.items(1)
        att = self.run_through(att, right=mc[:20], wrong=mc[20:30])
        self.assertIsNotNone(att.finished)
        self.assertEqual(att.mc_score, 20)
        s = exams.summary(att, self.pub)
        self.assertEqual((s["mc"], s["frq"], s["frq_parts_scored"]), (20, 0, 0))
        self.assertAlmostEqual(s["composite"], 24.0)
        self.assertEqual(s["ap"], 1)

    def test_composite_and_ap_estimate(self):
        cut = self.pub["cutoffs"]
        self.assertEqual([exams.ap_estimate(c, cut) for c in (108, 68, 67.9, 53, 52, 40, 39.5, 30, 29, 0)],
                         [5, 5, 4, 4, 3, 3, 2, 2, 1, 1])
        att = self.start()
        att = self.run_through(att, right=self.items(0) + self.items(1))                    # all 45 right: 54
        fps = exams.frq_parts(self.pub)
        q12 = [pt for q in self.pub["parts"][2]["items"] for pt in q["parts"]]
        self.assertEqual(fps[:len(q12)], q12)
        for p in q12:                                                                        # full marks on Questions 1 and 2
            n = len(self.priv["items"][p["id"]]["rubric"])
            self.assertEqual(self.api(att, "frq", part=p["id"], checks=[True] * n).status_code, 200)
        nxt = fps[len(q12)]["id"]                                                            # 1 point on the first part of Question 3
        r = self.api(att, "frq", part=nxt, checks=[True] + [False] * (len(self.priv["items"][nxt]["rubric"]) - 1)).json()
        s = r["summary"]
        self.assertEqual(s["mc"], 45)
        self.assertEqual(s["frq"], 18 + 1)
        self.assertAlmostEqual(s["composite"], 54 + 19)
        self.assertEqual(s["ap"], 5)
        self.assertEqual(s["frq_parts_scored"], len(q12) + 1)

    def test_frq_scores_only_after_the_exam_and_must_match_the_rubric(self):
        att = self.start()
        p = exams.frq_parts(self.pub)[0]
        n = len(self.priv["items"][p["id"]]["rubric"])
        self.assertEqual(self.api(att, "frq", part=p["id"], checks=[True] * n).status_code, 409)   # not finished
        att = self.run_through(att)
        self.assertEqual(self.api(att, "frq", part=p["id"], checks=[True] * (n + 1)).status_code, 409)
        self.assertEqual(self.api(att, "frq", part="nope", checks=[True]).status_code, 409)
        self.assertEqual(self.api(att, "frq", part=p["id"], checks=[True] * n).status_code, 200)

    def test_report_breaks_down_by_unit_and_links_lessons(self):
        att = self.start()
        mc = self.items(0) + self.items(1)
        att = self.run_through(att, right=mc[1:])                  # miss only question 1 (topic 1.6)
        units = exams.by_unit(att, self.pub)
        u1 = next(u for u in units if u["n"] == 1)
        self.assertEqual(u1["mc"], u1["mc_total"] - 1)
        self.assertEqual([r["n"] for r in u1["review"]], ["1.6"])
        self.assertEqual(sum(u["mc_total"] for u in units), 45)
        page = self.c.get(f"/exams/{SLUG}/attempt/{att.pk}/").content.decode()
        self.assertIn('"solution"', page)                         # the finished report carries the solutions
        home = self.c.get(f"/exams/{SLUG}/")
        self.assertContains(home, "Score report")

    def test_discard_only_unfinished(self):
        att = self.start()
        self.c.post(f"/exams/{SLUG}/attempt/{att.pk}/discard/")
        self.assertFalse(ExamAttempt.objects.filter(pk=att.pk).exists())
        att = self.run_through(self.start())
        self.c.post(f"/exams/{SLUG}/attempt/{att.pk}/discard/")
        self.assertTrue(ExamAttempt.objects.filter(pk=att.pk).exists())
