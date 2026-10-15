"""AB and BC versions (docs/ab-bc-versions.md): 6.14 is taught as 6.14 AB and 6.14 BC (6.15 internally), and Units 6-8
have an AB test (U6, U7, U8: no BC-only topics) and a BC test (U6BC, U7BC, U8BC: the whole unit)."""
import json
import re

from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Classroom, Enrollment, Profile, unit_of
from . import content
from .models import QuizAttempt

# words that only a BC-only topic of each unit would use (6.11-6.13, 7.5 and 7.9, 8.13)
BC_ONLY = {
    6: [r"by parts", r"partial fraction", r"\int u\,dv", r"improper", r"^\infty", r"diverge", "LIATE"],
    7: ["Euler", "logistic", "carrying capacity"],
    8: ["arc length", "length of the graph", "perimeter", r"\sqrt{1 + \left(\frac{dy}{dx}\right)^2}"],
}


def text(num):
    """Everything a student can be shown for a lesson or test, its answers and solutions too, as one lowercase string."""
    out = []

    def walk(v):
        if isinstance(v, str):
            out.append(v)
        elif isinstance(v, dict):
            for w in v.values():
                walk(w)
        elif isinstance(v, list):
            for w in v:
                walk(w)
    walk(content.public(num))
    walk(content.private(num))
    return "\n".join(out).lower()


class Labels(TestCase):
    def test_two_versions_of_6_14(self):
        self.assertEqual(content.label("6.14"), "6.14 AB")
        self.assertEqual(content.label("6.15"), "6.14 BC")
        self.assertTrue({"6.14", "6.15"} <= content.available())
        u, t = content.topic_meta("6.15")
        self.assertEqual((u["n"], t["bc"], t["tag"], t["short"], t["twin"]), (6, True, "BC", "6.14", "6.14"))
        self.assertEqual(content.topic_meta("6.14")[1]["tag"], "AB")
        self.assertEqual(content.topic_meta("6.11")[1]["tag"], "BC")       # other BC-only topics keep their tag
        self.assertEqual(content.topic_meta("9.1")[1]["tag"], "")          # a BC-only unit needs none on each lesson

    def test_test_versions(self):
        self.assertEqual([v["num"] for v in content.test_versions(6)], ["U6", "U6BC"])
        self.assertEqual([v["course"] for v in content.test_versions(7)], ["AB", "BC"])
        self.assertEqual(content.test_versions(4), [{"num": "U4", "course": ""}])
        self.assertEqual(content.test_label("U8BC"), "Unit 8 BC test")
        self.assertEqual(content.test_label("U8"), "Unit 8 AB test")
        self.assertEqual(content.test_label("U5"), "Unit 5 test")
        self.assertEqual(unit_of("U6BC"), 6)
        self.assertIn(6, content.unit_tests())

    def test_next_and_previous(self):
        nb = lambda n, c=None: tuple(x and x["n"] for x in content.neighbours(n, c))
        self.assertEqual(nb("6.13"), ("6.12", "6.15"))           # a BC lesson leads to the BC version
        self.assertEqual(nb("6.13", "AB"), ("6.12", "6.14"))     # an AB class goes to the AB version
        self.assertEqual(nb("6.10"), ("6.9", "6.11"))
        self.assertEqual(nb("6.14"), ("6.13", "U6"))             # each version skips its twin, to its own test
        self.assertEqual(nb("6.15"), ("6.13", "U6BC"))
        self.assertEqual(nb("6.15", "AB"), ("6.13", "U6"))
        self.assertEqual(nb("7.1"), (("6.14"), "7.2"))
        self.assertEqual(nb("7.1", "BC"), ("6.15", "7.2"))
        self.assertEqual(nb("7.9"), ("7.8", "U7BC"))
        self.assertEqual(nb("7.9", "AB"), ("7.8", "U7"))
        self.assertEqual(nb("8.13"), ("8.12", "U8BC"))
        self.assertEqual(nb("5.12"), ("5.11", "U5"))              # single-test units are unchanged


class Contents(TestCase):
    def test_ab_versions_leave_out_bc_only_topics(self):
        for num, unit in (("6.14", 6), ("U6", 6), ("U7", 7), ("U8", 8)):
            body = text(num)
            for word in BC_ONLY[unit]:
                self.assertNotIn(word.lower(), body, f"{num} mentions {word!r}")

    def test_bc_versions_include_them(self):
        for num, words in (("6.15", ["parts", "partial fractions"]), ("U6BC", ["Parts", "Partial fractions", r"^\infty"]),
                           ("U7BC", ["Euler", "logistic", "carrying capacity"]), ("U8BC", ["length of the graph", "perimeter"])):
            body = text(num)
            for word in words:
                self.assertIn(word.lower(), body, f"{num} lacks {word!r}")

    def test_versions_never_share_item_ids(self):
        # FRQ self-scores are keyed by part id alone, so an AB and a BC test must not share one
        for u in (6, 7, 8):
            ab, bc = set(content.private(f"U{u}")["items"]), set(content.private(f"U{u}BC")["items"])
            self.assertFalse(ab & bc)
            self.assertTrue(all(i.startswith(f"u{u}bc") for i in bc))
        self.assertFalse(set(content.private("6.14")["items"]) & set(content.private("6.15")["items"]))

    def test_same_format_and_forms(self):
        for u in (6, 7, 8):
            ab, bc = content.public(f"U{u}"), content.public(f"U{u}BC")
            self.assertEqual(len(ab["quiz_variants"]), len(bc["quiz_variants"]))
            self.assertEqual([len(r) for r in ab["frq_variants"]], [len(r) for r in bc["frq_variants"]])
            self.assertEqual((ab["version"], bc["version"]), ("AB", "BC"))


class Pages(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user("teach", password="pw123456")
        Profile.objects.create(user=self.teacher, role="teacher", display_name="Ms. Teach")
        self.ab = Classroom.objects.create(name="Period 3", teacher=self.teacher, course="AB")
        self.bc = Classroom.objects.create(name="Period 5", teacher=self.teacher, course="BC")

    def student(self, name, klass=None):
        u = User.objects.create_user(name, password="pw123456")
        Profile.objects.create(user=u, display_name=name.title(), full_access=klass is None)
        if klass:
            Enrollment.objects.create(classroom=klass, student=u)
        return u

    def test_course_map_and_menu_list_both(self):
        self.client.force_login(self.student("sol"))
        body = self.client.get("/course/").content.decode()
        for href in ('href="/topic/6.14/"', 'href="/topic/6.15/"', 'href="/unit/U6/test/"', 'href="/unit/U6BC/test/"',
                     'href="/unit/U7BC/test/"', 'href="/unit/U8BC/test/"', 'href="/unit/U9/test/"'):
            self.assertIn(href, body)
            # the map lists it, and the top bar's menu (on every page) lists it again
            self.assertGreaterEqual(body.count(href), 2, href)
        m = re.search(r'href="/topic/6.15/">\s*<span class="n">6.14</span>.*?</a>', body, re.S)
        self.assertIn('<span class="bc-tag">BC</span>', m.group(0))
        m = re.search(r'href="/topic/6.14/">\s*<span class="n">6.14</span>.*?</a>', body, re.S)
        self.assertIn('<span class="bc-tag">AB</span>', m.group(0))
        self.assertIn("Leaves out the BC-only topics", body)
        self.assertIn("The whole unit, BC topics included", body)

    def test_both_lessons_render_with_their_labels(self):
        self.client.force_login(self.student("sol"))
        for num, chip in (("6.14", "6.14 AB"), ("6.15", "6.14 BC")):
            for area in ("", "practice/", "quiz/", "testprep/"):
                r = self.client.get(f"/topic/{num}/{area}")
                self.assertContains(r, f'<span class="chip">{chip}</span>')
        r = self.client.get("/topic/6.15/")
        self.assertContains(r, 'href="/unit/U6BC/test/"')
        self.assertContains(self.client.get("/topic/6.14/"), 'href="/unit/U6/test/"')

    def test_class_course_picks_the_version(self):
        self.client.force_login(self.student("ana", self.ab))
        self.assertContains(self.client.get("/topic/6.13/"), 'href="/topic/6.14/"')
        self.assertContains(self.client.get("/topic/7.9/"), 'href="/unit/U7/test/"')
        self.client.force_login(self.student("bo", self.bc))
        self.assertContains(self.client.get("/topic/6.13/"), 'href="/topic/6.15/"')
        self.assertContains(self.client.get("/topic/7.1/"), 'href="/topic/6.15/"')

    def test_unit_test_page_offers_the_other_version(self):
        self.client.force_login(self.student("bo", self.bc))
        r = self.client.get("/unit/U6/test/")
        self.assertContains(r, 'href="/unit/U6BC/test/"')
        self.assertContains(r, "Your class takes the BC version.")
        self.assertContains(r, "Unit 6 AB test")
        r = self.client.get("/unit/U6BC/test/")
        self.assertContains(r, 'href="/unit/U6/test/"')
        self.assertContains(r, "<span class=\"chip\">U6 BC</span>")
        self.assertNotContains(self.client.get("/unit/U4/test/"), "test-versions")

    def test_bc_test_grades_and_shows_everywhere(self):
        stu = self.student("cy")
        self.client.force_login(stu)
        r = self.client.get("/unit/U7BC/test/")
        served = [q["id"] for q in r.context["lesson_json"]["quiz"]]
        keys = content.private("U7BC")["items"]
        r = self.client.post("/api/U7BC/quiz/", json.dumps({"answers": {i: keys[i]["answer"]["value"] for i in served}}),
                             content_type="application/json")
        self.assertEqual(r.json()["score"], len(served))
        self.assertEqual(QuizAttempt.objects.get().topic, "U7BC")
        part = next(i for i in keys if "rubric" in keys[i])
        self.assertEqual(self.client.post("/api/U7BC/frq/", json.dumps({"part": part, "earned": 1}), content_type="application/json").status_code, 200)
        # a saved result from before the split (U6 was always the AB test) shows as the AB version
        QuizAttempt.objects.create(user=stu, topic="U6", score=9, total=16, served=[], detail={})
        body = re.sub(r"\s+", " ", self.client.get("/course/").content.decode())
        self.assertRegex(body, r'href="/unit/U6/test/">[^<]*<span class="n">Test</span>.{0,300}AB.{0,300}best 9/16')
        self.assertRegex(body, r'href="/unit/U7BC/test/">[^<]*<span class="n">Test</span>.{0,300}BC.{0,300}best 16/16')
        r = self.client.get("/me/")
        self.assertContains(r, "Unit 7 BC test")
        self.assertContains(r, "Unit 6 AB test")

    def test_teacher_dashboard_and_release(self):
        stu = self.student("di", self.bc)
        QuizAttempt.objects.create(user=stu, topic="U8BC", score=10, total=16, served=[], detail={}, classroom=self.bc)
        self.client.force_login(self.teacher)
        r = self.client.get("/teacher/")
        self.assertContains(r, "Unit 8 BC test")
        self.assertContains(r, "Topic 6.14 BC")
        self.assertEqual(self.client.post(f"/teacher/class/{self.bc.pk}/release/U8BC/").status_code, 302)

    def test_handouts_list_both_versions(self):
        self.client.force_login(self.teacher)
        r = self.client.get("/teacher/handouts/")
        for href in ("/teacher/handouts/U6/U6-unittest-formA-classic.pdf", "/teacher/handouts/U6/U6-unittest-formA-key-classic.pdf",
                     "/teacher/handouts/U6BC/U6BC-unittest-formA-classic.pdf", "/teacher/handouts/U6BC/U6BC-unittest-formB-key-classic.pdf",
                     "/teacher/handouts/U7BC/U7BC-unittest-formA-classic.pdf", "/teacher/handouts/U8BC/U8BC-unittest-formA-key-classic.pdf",
                     "/teacher/handouts/6.14/6.14-notes-classic.pdf", "/teacher/handouts/6.15/6.15-notes-key-classic.pdf"):
            self.assertContains(r, href)
        self.assertContains(r, "Unit test, AB version")
        self.assertContains(r, "Unit test, BC version")
        self.assertContains(r, '<span class="chip-sm">6.14 BC</span>')
        pdf = self.client.get("/teacher/handouts/U6BC/U6BC-unittest-formA-classic.pdf")
        self.assertEqual(pdf["Content-Type"], "application/pdf")

    def test_solo_student_prints_the_bc_test(self):
        self.client.force_login(self.student("eve"))
        forms = self.client.get("/unit/U8BC/test/").context["state_json"]["print"]["forms"]
        self.assertEqual([f["form"] for f in forms], ["A", "B"])
        self.assertEqual(self.client.get(forms[1]["key"])["Content-Type"], "application/pdf")
