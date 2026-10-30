from django.contrib.auth.models import User
from django.test import Client, TestCase

from accounts.models import Classroom, Profile

from . import setup as S
from .models import Dated, Setup


def teacher(name="t1"):
    u = User.objects.create_user(name, password="pw12345678")
    Profile.objects.create(user=u, role=Profile.TEACHER, display_name=name.title())
    return u


class SettingsTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)

    def fresh(self):
        return Classroom.objects.get(pk=self.c.pk)          # drops the per-object setup cache

    def test_defaults_match_how_the_site_already_works(self):
        q = S.settings_for(self.c, "quiz", "2.5")
        self.assertEqual((q["where"], q["results"], q["attempts"]), ("site", "release", "one"))
        self.assertEqual(S.settings_for(self.c, "practice")["record"], "done")

    def test_class_then_unit_then_item_win_in_that_order(self):
        Setup.objects.create(classroom=self.c, kinds={"quiz": {"results": "now", "where": "paper"}},
                             units={"0": {"quiz": {"where": "off"}}})
        c = self.fresh()
        self.assertEqual(S.settings_for(c, "quiz", "2.5")["where"], "paper")
        self.assertEqual(S.settings_for(c, "quiz", "0.3")["where"], "off")
        d = Dated.objects.create(classroom=c, kind="quiz", ref="2.6", settings={"results": "due"})
        self.assertEqual(S.settings_for(c, "quiz", "2.6", d)["results"], "due")

    def test_practice_is_never_scored_for_correctness(self):
        self.assertEqual(S.clean("practice", {"record": "score"})["record"], "done")
        Setup.objects.create(classroom=self.c, kinds={"practice": {"record": "score"}})
        self.assertEqual(S.settings_for(self.fresh(), "practice")["record"], "done")

    def test_clean_drops_unknown_fields_and_values(self):
        self.assertEqual(S.clean("quiz", {"where": "moon", "results": "now", "x": "y"}), {"results": "now"})


class SetupPageTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)
        self.web = Client()
        self.web.force_login(self.t)
        self.url = f"/teacher/class/{self.c.pk}/setup/"

    def test_page_shows_every_kind(self):
        page = self.web.get(self.url).content.decode()
        for name in S.NAMES.values():
            self.assertIn(name, page)

    def test_saving_the_table(self):
        self.web.post(self.url, {"notes.where": "paper", "notes.record": "mark", "quiz.results": "now",
                                 "show.grade": "on", "watch.inactive": "on", "watch.inactive_days": "7"})
        s = Setup.objects.get(classroom=self.c)
        self.assertEqual((s.kinds["notes"]["where"], s.kinds["notes"]["record"], s.kinds["quiz"]["results"]), ("paper", "mark", "now"))
        self.assertEqual((s.show["grade"], s.show["due_dates"], s.watch["inactive_days"]), (True, False, 7))

    def test_a_template_fills_every_row(self):
        self.web.post(self.url, {"apply_template": "paper"})
        s = Setup.objects.get(classroom=self.c)
        self.assertEqual((s.kinds["notes"]["where"], s.kinds["unittest"]["where"], s.template), ("paper", "paper", "paper"))
        self.assertEqual(set(s.kinds), set(S.KINDS))

    def test_another_teachers_class_is_not_found(self):
        other = Client()
        other.force_login(teacher("t2"))
        self.assertEqual(other.get(self.url).status_code, 404)
        self.assertEqual(other.post(self.url, {"quiz.results": "now"}).status_code, 404)

    def test_students_are_turned_away(self):
        s = User.objects.create_user("kid", password="pw12345678")
        Profile.objects.create(user=s, display_name="Kid")
        web = Client()
        web.force_login(s)
        self.assertEqual(web.get(self.url).status_code, 403)


import datetime as dt  # noqa: E402

from . import calendar as cal  # noqa: E402
from .models import NoSchool, StudentException  # noqa: E402


class CalendarTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t, course="AB")
        Setup.objects.create(classroom=self.c, kinds=S.template_kinds("full_schedule"))
        self.c = Classroom.objects.get(pk=self.c.pk)

    def local(self, moment):
        return moment.astimezone(cal.zone(self.c))

    def test_unit_topics_follow_the_course(self):
        ab, bc = cal.unit_topics(6, "AB"), cal.unit_topics(6, "BC")
        self.assertNotIn("6.15", ab)            # 6.14 BC is stored as 6.15
        self.assertIn("6.15", bc)
        self.assertLess(len(cal.unit_topics(10, "AB")), 1)   # Unit 10 is BC only

    def test_planning_skips_weekends_and_no_school(self):
        NoSchool.objects.create(classroom=self.c, day=dt.date(2026, 10, 21))     # a Wednesday
        rows = cal.plan_unit(self.c, 2, dt.date(2026, 10, 17))                   # a Saturday: starts Monday
        notes = sorted((d for d in rows if d.kind == "notes"), key=lambda d: d.opens)
        days = [self.local(d.opens).date() for d in notes]
        self.assertEqual(days[0], dt.date(2026, 10, 19))
        self.assertNotIn(dt.date(2026, 10, 21), days)
        self.assertTrue(all(d.weekday() < 5 for d in days))
        quiz = next(d for d in rows if d.kind == "quiz" and d.ref == notes[0].ref)
        self.assertEqual(self.local(quiz.due).date(), dt.date(2026, 10, 20))      # due the next class day
        self.assertEqual((self.local(quiz.due).hour, self.local(quiz.due).minute), (23, 59))
        self.assertTrue(any(d.kind == "unittest" for d in rows))

    def test_planning_only_dates_what_setup_schedules(self):
        Setup.objects.filter(classroom=self.c).update(kinds={})          # the defaults: nothing on a schedule
        c = Classroom.objects.get(pk=self.c.pk)
        self.assertEqual(cal.plan_unit(c, 2, dt.date(2026, 10, 19)), [])

    def test_a_snow_day_moves_later_work_one_class_day(self):
        cal.plan_unit(self.c, 2, dt.date(2026, 10, 19))
        fri = Dated.objects.get(classroom=self.c, kind="notes", ref="2.5")      # Fri Oct 23
        cal.shift(self.c, dt.date(2026, 10, 23), 1)
        fri.refresh_from_db()
        self.assertEqual(self.local(fri.opens).date(), dt.date(2026, 10, 26))   # over the weekend to Monday
        first = Dated.objects.get(classroom=self.c, kind="notes", ref="2.1")
        self.assertEqual(self.local(first.opens).date(), dt.date(2026, 10, 19))  # earlier work stays


class CalendarPageTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)
        self.web = Client()
        self.web.force_login(self.t)
        self.url = f"/teacher/class/{self.c.pk}/calendar/"
        self.kid = User.objects.create_user("kid", password="pw12345678")
        Profile.objects.create(user=self.kid, display_name="Kid")
        self.c.enrollments.create(student=self.kid)

    def test_add_a_date_and_an_exception(self):
        self.web.post(self.url, {"action": "add", "kind": "quiz", "ref": "2.5"})
        d = Dated.objects.get(classroom=self.c, kind="quiz", ref="2.5")
        self.web.post(self.url, {"action": "item", "dated": d.pk, "opens": "2026-11-02T08:00", "due": "2026-11-03T23:59", "results": "now"})
        d.refresh_from_db()
        self.assertEqual(self.local_hm(d.due), (23, 59))
        self.assertEqual(d.settings, {"results": "now"})
        self.web.post(self.url, {"action": "exc_add", "dated": d.pk, "student": self.kid.pk, "due": "2026-11-06T23:59", "time_factor": "1.5"})
        e = StudentException.objects.get(dated=d)
        self.assertEqual((e.student, e.time_factor), (self.kid, 1.5))
        self.assertIn("Quiz 2.5", self.web.get(self.url + "?start=2026-11-02").content.decode())

    def local_hm(self, m):
        m = m.astimezone(cal.zone(self.c))
        return m.hour, m.minute

    def test_unknown_refs_and_other_classes_are_refused(self):
        self.web.post(self.url, {"action": "add", "kind": "quiz", "ref": "99.9"})
        self.assertFalse(Dated.objects.exists())
        other = Classroom.objects.create(name="P5", teacher=teacher("t2"))
        d = Dated.objects.create(classroom=other, kind="quiz", ref="2.5")
        self.web.post(self.url, {"action": "item_delete", "dated": d.pk})
        self.assertTrue(Dated.objects.filter(pk=d.pk).exists())

    def test_the_return_address_stays_on_the_page(self):
        r = self.web.post(self.url, {"action": "noschool", "day": "2026-11-26", "back": "//evil.example/"})
        self.assertEqual(r["Location"], self.url)


import json  # noqa: E402

from django.utils import timezone  # noqa: E402

from course.models import QuizAttempt  # noqa: E402

from .access import gate  # noqa: E402


class StudentGateTests(TestCase):
    """What a class's setup and calendar do to one student's pages."""

    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)
        self.kid = User.objects.create_user("kid", password="pw12345678")
        Profile.objects.create(user=self.kid, display_name="Kid")
        self.c.enrollments.create(student=self.kid)
        self.web = Client()
        self.web.force_login(self.kid)
        self.now = timezone.now()

    def configure(self, **kinds):
        Setup.objects.update_or_create(classroom=self.c, defaults={"kinds": kinds})

    def date(self, kind, ref="2.5", opens=None, due=None, **kw):
        return Dated.objects.create(classroom=self.c, kind=kind, ref=ref, opens=opens, due=due, **kw)

    def quiz_post(self):
        return self.web.post("/api/2.5/quiz/", json.dumps({"answers": {}}), content_type="application/json")

    def test_nothing_changes_for_a_class_nobody_set_up(self):
        self.assertEqual(gate(self.kid, "quiz", "2.5")["state"], "open")
        self.assertEqual(self.web.get("/topic/2.5/quiz/").status_code, 200)

    def test_a_scheduled_quiz_waits_for_its_open_date(self):
        self.configure(quiz={"opens": "schedule", "dates": "dated"})
        self.date("quiz", opens=self.now + dt.timedelta(days=2), due=self.now + dt.timedelta(days=3))
        page = self.web.get("/topic/2.5/quiz/").content.decode()
        self.assertIn("opens", page)
        self.assertNotIn('id="app"', page)
        self.assertEqual(self.quiz_post().status_code, 403)

    def test_a_locked_quiz_closes_at_its_due_date_unless_reopened(self):
        self.configure(quiz={"dates": "dated", "late": "lock"})
        d = self.date("quiz", due=self.now - dt.timedelta(hours=1))
        self.assertEqual(self.quiz_post().status_code, 409)
        self.assertIn("closed", self.web.get("/topic/2.5/quiz/").content.decode())
        StudentException.objects.create(dated=d, student=self.kid, due=self.now + dt.timedelta(days=2))
        self.assertEqual(gate(self.kid, "quiz", "2.5")["state"], "open")
        self.assertEqual(self.quiz_post().status_code, 200)

    def test_late_work_is_accepted_and_marked(self):
        self.configure(quiz={"dates": "dated", "late": "marked"})
        self.date("quiz", due=self.now - dt.timedelta(hours=1))
        g = gate(self.kid, "quiz", "2.5")
        self.assertEqual((g["state"], g["late"]), ("open", True))

    def test_results_follow_the_setup(self):
        self.quiz_post()
        self.assertFalse(json.loads(self.quiz_post().content).get("score") is not None)   # default: wait for release
        self.configure(quiz={"results": "now"})
        QuizAttempt.objects.all().delete()
        r = json.loads(self.quiz_post().content)
        self.assertTrue(r["released"])

    def test_best_of_unlimited_allows_retakes(self):
        self.configure(quiz={"attempts": "best"})
        self.assertEqual(self.quiz_post().status_code, 200)
        self.assertEqual(self.quiz_post().status_code, 200)
        self.configure(quiz={"attempts": "one"})
        self.assertEqual(self.quiz_post().status_code, 409)

    def test_paper_and_unused_quizzes_say_so(self):
        self.configure(quiz={"where": "paper"})
        self.assertIn("on paper", self.web.get("/topic/2.5/quiz/").content.decode())
        self.configure(quiz={"where": "off"})
        self.assertIn("use this quiz on the site", self.web.get("/topic/2.5/quiz/").content.decode())

    def test_closed_practice_stops_checking(self):
        self.configure(practice={"dates": "dated", "late": "lock"})
        self.date("practice", due=self.now - dt.timedelta(hours=1))
        pub = __import__("course.content", fromlist=["public"]).public("2.5")
        r = self.web.post("/api/2.5/check/", json.dumps({"item": pub["practice"][0]["id"], "given": "1", "area": "practice"}),
                          content_type="application/json")
        self.assertEqual(r.status_code, 403)

    def test_due_date_shows_on_the_lesson(self):
        self.configure(practice={"dates": "dated"})
        self.date("practice", due=self.now + dt.timedelta(days=1))
        self.assertIn("due-line", self.web.get("/topic/2.5/practice/").content.decode())

    def test_people_outside_a_class_are_never_gated(self):
        self.configure(quiz={"where": "off"})
        solo = User.objects.create_user("solo", password="pw12345678")
        Profile.objects.create(user=solo, display_name="Solo", full_access=True)
        self.assertEqual(gate(solo, "quiz", "2.5")["state"], "open")


from .models import AnswerFix, GraderMiss  # noqa: E402
from .progress import ClassData  # noqa: E402


class DashboardTests(TestCase):
    def setUp(self):
        self.t = teacher()
        self.c = Classroom.objects.create(name="P3", teacher=self.t)
        self.web = Client()
        self.web.force_login(self.t)
        self.kids = []
        for i in range(4):
            k = User.objects.create_user(f"kid{i}", password="pw12345678")
            Profile.objects.create(user=k, display_name=f"Kid {i}")
            self.c.enrollments.create(student=k)
            self.kids.append(k)
        pub = __import__("course.content", fromlist=["public"]).public("2.5")
        rows = pub.get("quiz_variants") or [[q] for q in pub["quiz"]]
        self.served = [r[0]["id"] for r in rows]
        for i, k in enumerate(self.kids):          # everyone gets question 1 wrong with the same answer
            det = {sid: {"given": "2x" if j == 0 else "ok", "correct": j != 0 and i % 2 == 0} for j, sid in enumerate(self.served)}
            QuizAttempt.objects.create(user=k, topic="2.5", score=sum(d["correct"] for d in det.values()), total=len(self.served),
                                       served=self.served, detail=det, classroom=self.c, form="A")
        self.base = f"/teacher/class/{self.c.pk}/"

    def score(self, k):
        return ClassData(Classroom.objects.get(pk=self.c.pk)).quiz(k.id, "2.5")

    def test_every_page_loads(self):
        for path in ("", "progress/", "quizzes/", "quizzes/2.5/", "students/", f"students/{self.kids[0].pk}/", "calendar/", "setup/"):
            self.assertEqual(self.web.get(self.base + path).status_code, 200, path)

    def test_home_flags_results_to_release_and_a_hard_question(self):
        page = self.web.get(self.base).content.decode()
        self.assertIn("Results are waiting", page)
        self.assertIn("question 1", page)

    def test_accepting_an_answer_fixes_everyone_who_gave_it(self):
        before = self.score(self.kids[0])
        self.web.post(self.base + "quizzes/2.5/", {"action": "accept", "item": self.served[0], "given": "2x"})
        self.assertEqual(AnswerFix.objects.count(), 4)
        self.assertEqual(self.score(self.kids[0])[0], before[0] + 1)
        self.assertTrue(GraderMiss.objects.filter(topic="2.5", given="2x").exists())

    def test_marking_one_answer_and_half_credit(self):
        k = self.kids[1]
        url = self.base + f"students/{k.pk}/"
        before = self.score(k)[0]
        self.web.post(url, {"action": "half", "ref": "2.5", "item": self.served[1]})
        self.assertEqual(self.score(k)[0], before + 0.5)
        self.web.post(url, {"action": "unfix", "ref": "2.5", "item": self.served[1]})
        self.assertEqual(self.score(k)[0], before)

    def test_dropping_a_question_shrinks_the_total(self):
        self.web.post(self.base + "quizzes/2.5/", {"action": "drop", "item": self.served[0]})
        self.assertEqual(self.score(self.kids[0])[1], len(self.served) - 1)

    def test_release_toggles(self):
        from course.models import Release
        self.web.post(self.base + "quizzes/2.5/", {"action": "release"})
        self.assertTrue(Release.objects.filter(classroom=self.c, topic="2.5").exists())

    def test_another_teacher_sees_nothing(self):
        other = Client()
        other.force_login(teacher("t2"))
        for path in ("", "progress/", "quizzes/2.5/", f"students/{self.kids[0].pk}/"):
            self.assertEqual(other.get(self.base + path).status_code, 404, path)
        other.post(self.base + "quizzes/2.5/", {"action": "accept", "item": self.served[0], "given": "2x"})
        self.assertFalse(AnswerFix.objects.exists())


from . import grades as G  # noqa: E402
from .models import Category, Curve, Mark, TeacherItem  # noqa: E402


class GradebookTests(DashboardTests):
    """Same class as DashboardTests: four students, Quiz 2.5 taken by all (kids 0 and 2 did better)."""

    def book(self):
        return G.Book(Classroom.objects.get(pk=self.c.pk))

    def cat(self, src):
        return next(c for c in self.book().cats if c.source == src)

    def test_defaults_and_shared_weights(self):
        b = self.book()
        self.assertEqual([c.source for c in b.cats], ["unittest", "quiz", "practice", "exam"])
        q = b.category(self.cat("quiz"), self.kids[0].id)
        self.assertAlmostEqual(b.final(self.kids[0].id), round(100 * q, 1))     # only quizzes have items: they're the grade

    def test_drop_lowest_and_missing_past_due_counts_zero(self):
        Dated.objects.create(classroom=self.c, kind="quiz", ref="2.6", due=timezone.now() - dt.timedelta(days=1))
        Setup.objects.create(classroom=self.c, kinds={"quiz": {"dates": "dated"}})
        k = self.kids[0].id
        self.assertEqual(self.book().raw(self.cat("quiz"), k, "2.6"), 0.0)
        c = self.cat("quiz")
        c.rules = {"drop_lowest": 1}
        c.save()
        b = self.book()
        self.assertEqual(b.category(c, k), b.raw(c, k, "2.5"))

    def test_practice_counts_completion_not_correctness(self):
        pub = __import__("course.content", fromlist=["public"]).public("2.5")
        from course.models import Response
        for it in pub["practice"]:
            Response.objects.create(user=self.kids[1], topic="2.5", item=it["id"], area="practice", given="0", correct=False)
        self.assertEqual(self.book().raw(self.cat("practice"), self.kids[1].id, "2.5"), 1.0)

    def test_curves_never_lower_a_score(self):
        Curve.objects.create(classroom=self.c, kind="quiz", ref="2.5", method="mean", params={"target": 90})
        b = self.book()
        for k in self.kids:
            self.assertGreaterEqual(b.score(self.cat("quiz"), k.id, "2.5"), b.raw(self.cat("quiz"), k.id, "2.5"))
            self.assertLessEqual(b.score(self.cat("quiz"), k.id, "2.5"), 1.0)

    def test_own_items_and_entry_page(self):
        self.web.post(self.base + "gradebook/", {"action": "add_category", "name": "Participation", "source": "own", "weight": "10"})
        cat = Category.objects.get(classroom=self.c, source="own")
        self.web.post(self.base + "gradebook/", {"action": "add_item", "cat": cat.pk, "name": "Week 1", "points": "10"})
        it = TeacherItem.objects.get(category=cat)
        self.web.post(self.base + "gradebook/enter/", {"item": f"own:{it.pk}", f"v{self.kids[0].pk}": "8", f"v{self.kids[1].pk}": "ex"})
        b = self.book()
        own = next(c for c in b.cats if c.source == "own")
        self.assertEqual(b.raw(own, self.kids[0].id, f"own{it.pk}"), 0.8)
        self.assertIsNone(b.raw(own, self.kids[1].id, f"own{it.pk}"))

    def test_paper_unit_test_parts_and_absent(self):
        url = self.base + "gradebook/enter/"
        k0, k1 = self.kids[0].pk, self.kids[1].pk
        parts = G.test_parts("U2")
        data = {"item": "unittest:U2", f"p{k0}.mc": "10", f"p{k0}.frq1": "5", f"x{k1}": "ab"}
        self.web.post(url, data)
        q = ClassData(Classroom.objects.get(pk=self.c.pk)).quiz(k0, "U2")
        self.assertEqual(q, (15.0, sum(p[2] for p in parts[:2])))
        self.assertIsNone(self.book().raw(self.cat("unittest"), k1, "U2"))
        self.assertTrue(Mark.objects.filter(student_id=k1, ref="U2", absent=True).exists())

    def test_exports(self):
        for fmt in ("totals", "items", "powerschool"):
            r = self.web.get(self.base + f"gradebook/{fmt}.csv")
            self.assertEqual(r.status_code, 200)
            self.assertIn("Kid 0", r.content.decode())

    def test_another_teacher_cannot_export_or_enter(self):
        other = Client()
        other.force_login(teacher("t3"))
        self.assertEqual(other.get(self.base + "gradebook/totals.csv").status_code, 404)
        self.assertEqual(other.get(self.base + "gradebook/").status_code, 404)


class StudentPageTests(DashboardTests):
    def test_unreleased_scores_stay_hidden_on_me(self):
        web = Client()
        web.force_login(self.kids[0])
        page = web.get("/me/").content.decode()
        self.assertIn("waiting for your teacher", page)
        self.assertNotIn("Your grade", page)                 # the only scores aren't released: no grade from them
        from course.models import Release
        Release.objects.create(classroom=self.c, topic="2.5")
        self.assertIn("Your grade", web.get("/me/").content.decode())

    def test_grade_hidden_when_setup_says_so(self):
        from course.models import Release
        Release.objects.create(classroom=self.c, topic="2.5")
        Setup.objects.create(classroom=self.c, show={"grade": False})
        web = Client()
        web.force_login(self.kids[0])
        self.assertNotIn("Your grade", web.get("/me/").content.decode())
