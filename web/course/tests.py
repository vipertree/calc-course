import json
import re

from django.contrib.auth.models import User
from django.test import Client, TestCase

from accounts.models import Classroom, Enrollment, Profile
from . import content, grading, packets
from .models import FRQScore, QuizAttempt, Response


class Grading(TestCase):
    def test_equivalent_expressions(self):
        spec = {"kind": "expr", "value": "2*x+2", "var": "x"}
        self.assertTrue(grading.check("2(x+1)", spec))
        self.assertTrue(grading.check("2x+2", spec))
        self.assertFalse(grading.check("2x+1", spec))
        self.assertTrue(grading.check("1/(2 sqrt(x))", {"kind": "expr", "value": "x**(-1/2)/2"}))

    def test_equation_forms(self):
        spec = {"kind": "expr", "value": "6*x-9", "var": "x"}
        self.assertTrue(grading.check("y=6x-9", spec))
        self.assertTrue(grading.check("y = 6(x-3)+9", spec))
        self.assertTrue(grading.check("f'(x)=6x-9", spec))
        self.assertFalse(grading.check("y=6x+9", spec))

    def test_forgiving_input(self):
        units = {"kind": "number", "value": "-3/2", "tol": 0, "display": r"-1.5\ \text{gal/min}^2"}
        for g in ("-1.5", "-1.5 gal/min^2", "−1.5", "-3/2 gal/min²", r"\frac{-3}{2}\text{gal/min}^2"):
            self.assertTrue(grading.check(g, units), g)
        self.assertFalse(grading.check("40x", {"kind": "number", "value": "40", "tol": 0}))
        self.assertTrue(grading.check("1,200", {"kind": "number", "value": "1200", "tol": 0}))
        self.assertTrue(grading.check("k = 2.", {"kind": "number", "value": "2", "tol": 0}))
        line = {"kind": "expr", "value": "12*x-16", "var": "x"}
        for g in ("y-8=12(x-2)", "y = 12x - 16", "dy/dx = 12x-16"):
            self.assertTrue(grading.check(g, line), g)
        self.assertFalse(grading.check("y-8=12(x+2)", line))
        self.assertTrue(grading.check("Sin(x)+cosx", {"kind": "expr", "value": "sin(x)+cos(x)", "var": "x"}))
        inv = {"kind": "expr", "value": "asin(x) + x/sqrt(1-x**2)", "var": "x"}   # keys use sympy names; students type arcsin or sin^-1
        for g in ("arcsin(x) + x/sqrt(1-x^2)", "sin^(-1)(x) + x/sqrt(1-x^2)"):
            self.assertTrue(grading.check(g, inv), g)
        self.assertFalse(grading.check("arctan(x) + x/sqrt(1-x^2)", inv))

    def test_numbers_and_tolerance(self):
        exact = {"kind": "number", "value": "-27/7", "tol": 0}
        self.assertTrue(grading.check("(-27)/(7)", exact))
        self.assertTrue(grading.check("-3.857", exact))      # three decimal places, the AP standard
        self.assertFalse(grading.check("-3.86", exact))
        loose = {"kind": "number", "value": "-27/7", "tol": 0.005}
        self.assertTrue(grading.check("-3.857", loose))
        self.assertFalse(grading.check("-3.85", loose))
        self.assertTrue(grading.check("8.0", {"kind": "number", "value": "8", "tol": 0}))
        self.assertFalse(grading.check("x", {"kind": "number", "value": "8", "tol": 0}))

    def test_mathlive_ascii_forms(self):
        self.assertTrue(grading.check("(1)/(4)", {"kind": "number", "value": "1/4", "tol": 0}))
        self.assertTrue(grading.check("sqrt(16)", {"kind": "number", "value": "4", "tol": 0}))
        self.assertTrue(grading.check("e^(x)", {"kind": "expr", "value": "exp(x)"}))
        self.assertTrue(grading.check("π/2", {"kind": "number", "value": "pi/2", "tol": 0}))
        self.assertTrue(grading.check(".5", {"kind": "number", "value": "1/2", "tol": 0}))

    def test_dne_and_infinity(self):
        dne = {"kind": "number", "value": "DNE", "tol": 0}
        for ok in ["DNE", "dne", "does not exist", "D N E"]:
            self.assertTrue(grading.check(ok, dne), ok)
        self.assertFalse(grading.check("0", dne))
        inf = {"kind": "number", "value": "oo", "tol": 0}
        self.assertTrue(grading.check("∞", inf))
        self.assertTrue(grading.check("infinity", inf))
        self.assertFalse(grading.check("-∞", inf))
        self.assertFalse(grading.check("DNE", inf))
        self.assertFalse(grading.check("DNE", {"kind": "number", "value": "3", "tol": 0}))

    def test_rejects_code(self):
        for bad in ["__import__('os')", "x.__class__", "lambda: 1", "a" * 400, "open('f')"]:
            self.assertFalse(grading.check(bad, {"kind": "expr", "value": "x"}))

    def test_blanks(self):
        self.assertTrue(grading.check_blank("secant", "secant"))
        self.assertTrue(grading.check_blank("The Secant", "secant"))
        self.assertTrue(grading.check_blank("slope of tangent line", "slope of the tangent line"))
        self.assertTrue(grading.check_blank("instantaneous rate of chnage", "instantaneous rate of change"))
        self.assertFalse(grading.check_blank("tangent", "secant"))
        self.assertTrue(grading.check_blank("25/4", "$6.25$"))
        self.assertTrue(grading.check_blank("9", "$9$"))


class AnswerKeys(TestCase):
    """Every stored answer must be accepted by the grader when typed back in. Catches unparseable keys."""

    def test_every_key_grades_itself(self):
        bad = []
        for num in sorted(content.available()) + [f"U{n}" for n in sorted(content.unit_tests())]:
            for iid, spec in content.private(num)["items"].items():
                ans = spec.get("answer")
                if not ans or ans["kind"] in ("self",):
                    continue
                given = ans["value"]
                if ans["kind"] == "number" and given not in ("DNE", "oo", "-oo"):
                    given = str(given)
                if not grading.check(given, ans):
                    bad.append(f"{num} {iid}: {given!r}")
            for bid, key in content.private(num)["blanks"].items():
                typed = key.strip().strip("$")
                if key.strip().startswith("$") and not grading.check_blank(typed, key):
                    bad.append(f"{num} blank {bid}: {key!r}")
        self.assertEqual(bad, [])


class Flow(TestCase):
    def setUp(self):
        t = User.objects.create_user("teach", password="pw123456")
        Profile.objects.create(user=t, role="teacher", display_name="Ms. Teach")
        self.c = Classroom.objects.create(name="Period 3", teacher=t)

    def join(self, name="ana"):
        return self.client.post("/join/", {"code": self.c.code.lower(), "display_name": "Ana Ruiz", "username": name,
                                           "password": "pw123456"})

    def test_join_with_code_and_see_lesson(self):
        r = self.join()
        self.assertEqual(r.status_code, 302)
        self.assertTrue(Enrollment.objects.filter(classroom=self.c, student__username="ana").exists())
        r = self.client.get("/topic/2.1/")
        self.assertContains(r, "Average and Instantaneous Rates of Change")
        # answers never reach the page
        priv = content.private("2.1")
        body = r.content.decode()
        self.assertNotIn("private", body)
        self.assertNotIn(json.dumps(priv["items"]["p2_1-4"]["solution"])[1:40], body)

    def test_closed_class_rejects(self):
        self.c.open = False
        self.c.save()
        r = self.join()
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username="ana").exists())

    def test_check_quiz_frq(self):
        self.join()
        r = self.client.post("/api/2.1/check/", json.dumps({"item": "p2_1-1", "given": "11", "area": "practice"}),
                             content_type="application/json")
        self.assertTrue(r.json()["correct"])
        self.assertIn("solution", r.json())
        r = self.client.post("/api/2.1/check/", json.dumps({"item": "n2_1-b3", "given": "10"}), content_type="application/json")
        self.assertTrue(r.json()["correct"])
        page = self.client.get("/topic/2.1/quiz/").content.decode()
        served = [q["id"] for q in json.loads(re.search(r'<script id="lesson" type="application/json">(.*?)</script>', page, re.S).group(1))["quiz"]]
        keys = content.private("2.1")["items"]
        answers = {i: keys[i]["answer"]["value"] for i in served[:2]}          # the first two right, the rest blank
        r = self.client.post("/api/2.1/quiz/", json.dumps({"answers": answers}), content_type="application/json")
        self.assertEqual(r.json(), {"submitted": True, "released": False})   # class students wait for release
        self.assertEqual(QuizAttempt.objects.get().score, 2)                   # but it is graded and stored
        r = self.client.post("/api/2.1/frq/", json.dumps({"part": "f2_1-1a", "earned": 9}), content_type="application/json")
        self.assertEqual(r.json(), {"earned": 2, "possible": 2})   # clamped to the rubric
        self.assertEqual(FRQScore.objects.get().earned, 2)
        self.assertEqual(Response.objects.count(), 2)

    def test_teacher_dashboard(self):
        self.join()
        self.client.logout()
        self.client.login(username="teach", password="pw123456")
        r = self.client.get("/teacher/")
        self.assertContains(r, "Ana Ruiz")
        self.assertContains(r, self.c.code)

    def test_unit_test_page_and_grading(self):
        self.join()
        r = self.client.get("/unit/U1/test/")
        self.assertContains(r, "Limits and Continuity")
        self.assertNotIn("private", r.content.decode())
        # the class form depends on the (random) join code, so answer from the form actually served:
        # first question right, second wrong
        served = [q["id"] for q in r.context["lesson_json"]["quiz"]]
        keys = content.private("U1")["items"]
        right = keys[served[0]]["answer"]["value"]
        wrong = next(c for c in "ABCD" if c != keys[served[1]]["answer"]["value"])
        r = self.client.post("/api/U1/quiz/", json.dumps({"answers": {served[0]: right, served[1]: wrong}}),
                             content_type="application/json")
        self.assertEqual(r.json(), {"submitted": True, "released": False})
        self.assertEqual(QuizAttempt.objects.get().score, 1)
        # class students' unit-test FRQ answers are saved, not graded, and self-scoring waits too
        r = self.client.post("/api/U1/check/", json.dumps({"item": "u1f1a", "given": "3", "area": "frq"}),
                             content_type="application/json")
        self.assertEqual(r.json(), {"saved": True})
        self.assertEqual(self.client.post("/api/U1/frq/", json.dumps({"part": "u1f1a", "earned": 1}),
                                          content_type="application/json").status_code, 403)
        self.assertContains(self.client.get("/course/"), "Unit 1 test")

    def test_every_lesson_page_renders(self):
        self.join()
        for num in sorted(content.available()):
            for area in ("", "practice/", "quiz/", "testprep/"):
                r = self.client.get(f"/topic/{num}/{area}")
                self.assertEqual(r.status_code, 200, f"{num} {area}")

    def test_transcripts_teacher_only(self):
        self.client.login(username="teach", password="pw123456")
        r = self.client.get("/teacher/transcripts/?t=1.1")
        self.assertContains(r, "Can Change Occur at an Instant")
        self.assertContains(r, "the flying arrow is therefore motionless")
        self.client.logout()
        self.join()
        self.assertEqual(self.client.get("/teacher/transcripts/").status_code, 403)

    def test_visitor_preview(self):
        r = self.client.get("/topic/2.1/")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertIn('"preview": true', body)
        self.assertNotIn("Shrinking the interval", body)          # notes stay on the server
        self.assertIn("From average to instant", body)            # the video is free
        r = self.client.get("/topic/2.1/practice/")
        self.assertEqual(body.count("p2_1-5"), 0)
        ok = self.client.post("/api/2.1/check/", json.dumps({"item": "p2_1-1", "given": "11", "area": "practice"}),
                              content_type="application/json")
        self.assertTrue(ok.json()["correct"])
        self.assertEqual(Response.objects.count(), 0)              # nothing saved for visitors
        no = self.client.post("/api/2.1/check/", json.dumps({"item": "p2_1-6", "given": "1", "area": "practice"}),
                              content_type="application/json")
        self.assertEqual(no.status_code, 403)
        self.assertContains(self.client.get("/unit/U1/test/"), "for members")
        self.assertEqual(self.client.get("/course/").status_code, 200)

    def test_student_cannot_see_dashboard(self):
        self.join()
        self.assertEqual(self.client.get("/teacher/").status_code, 403)


class Designs(TestCase):
    def test_design_switch(self):
        from pathlib import Path
        from django.conf import settings
        from .context import DESIGNS
        page = self.client.get("/course/").content.decode()
        self.assertNotIn("data-design", page)                 # classic renders the original markup
        self.assertNotIn("css/designs/", page)
        for key, _ in DESIGNS[1:]:
            css = Path(settings.BASE_DIR) / "static" / "css" / "designs" / f"{key}.css"
            self.assertTrue(css.exists(), key)
            text = css.read_text()
            for bad in ("alert(", "confirm(", "prompt("):
                self.assertNotIn(bad, text)
            r = self.client.get(f"/design/{key}/?next=/course/")
            self.assertEqual(r.status_code, 302)
            page = self.client.get("/course/").content.decode()
            self.assertIn(f'data-design="{key}"', page)
            self.assertIn(f"css/designs/{key}.css", page)
        self.client.get("/design/nonsense/?next=/course/")     # unknown names are ignored
        self.assertIn('data-design="chalk"', self.client.get("/course/").content.decode())
        self.client.cookies["design"] = "../evil"
        self.assertNotIn("data-design", self.client.get("/course/").content.decode())

    def test_transit_map_columns(self):
        self.client.get("/design/transit/?next=/course/")
        page = self.client.get("/course/").content.decode()
        self.assertNotIn("map-layout", page)                     # one layout, no toggle
        self.assertNotIn("data-layout", page)
        self.assertEqual(self.client.get("/map-layout/rows/").status_code, 404)


class Assessments(TestCase):
    """Quiz variants: individual users draw per attempt with instant results; a class shares one form and
    waits for the teacher to release results."""

    def setUp(self):
        self.teacher = User.objects.create_user("teach", password="pw123456")
        Profile.objects.create(user=self.teacher, role="teacher", display_name="Ms. Teach")
        self.c = Classroom.objects.create(name="Period 3", teacher=self.teacher)
        self.pub = content.public("1.1")

    def student(self, name, in_class=True):
        u = User.objects.create_user(name, password="pw123456")
        Profile.objects.create(user=u, display_name=name.title(), full_access=not in_class)
        if in_class:
            Enrollment.objects.create(classroom=self.c, student=u)
        return u

    def served(self, client):
        r = client.get("/topic/1.1/quiz/")
        m = re.search(r'<script id="lesson" type="application/json">(.*?)</script>', r.content.decode(), re.S)
        L = json.loads(m.group(1))
        return [q["id"] for q in L["quiz"]], r

    def test_page_holds_only_served_versions(self):
        self.client.force_login(self.student("ivy", in_class=False))
        ids, r = self.served(self.client)
        body = r.content.decode()
        self.assertEqual(len(ids), len(self.pub["quiz_variants"]))
        self.assertNotIn("quiz_variants", body)
        others = {v["id"] for row in self.pub["quiz_variants"] for v in row} - set(ids)
        for o in others:
            self.assertNotIn(f'"{o}"', body)
        self.assertEqual(self.served(self.client)[0], ids)          # a reload keeps the same draw

    def test_individual_gets_instant_results_and_a_fresh_draw(self):
        self.client.force_login(self.student("ivy", in_class=False))
        draws = set()
        for _ in range(6):
            ids, _ = self.served(self.client)
            draws.add(tuple(ids))
            r = self.client.post("/api/1.1/quiz/", json.dumps({"answers": {}}), content_type="application/json")
            self.assertIn("score", r.json())
            self.assertEqual(set(r.json()["detail"]), set(ids))    # graded exactly what was served
        self.assertGreater(len(draws), 1)

    def test_class_shares_one_form_and_waits_for_release(self):
        a, b = Client(), Client()
        a.force_login(self.student("ana"))
        b.force_login(self.student("ben"))
        ids_a, _ = self.served(a)
        ids_b, _ = self.served(b)
        self.assertEqual(ids_a, ids_b)
        r = a.post("/api/1.1/quiz/", json.dumps({"answers": {}}), content_type="application/json")
        self.assertEqual(r.json(), {"submitted": True, "released": False})
        self.assertNotIn("score", r.json())
        r = a.post("/api/1.1/quiz/", json.dumps({"answers": {}}), content_type="application/json")
        self.assertEqual(r.status_code, 409)                        # one submission per class student
        _, page = self.served(a)
        self.assertNotIn("solution", json.dumps(page.context["state_json"]))
        t = Client()
        t.force_login(self.teacher)
        self.assertContains(t.get("/teacher/"), "Release results")
        t.post(f"/teacher/class/{self.c.pk}/release/1.1/")
        state = self.served(a)[1].context["state_json"]["assess"]
        self.assertTrue(state["released"])
        self.assertEqual(set(state["result"]["detail"]), set(ids_a))


class Video(TestCase):
    """Videos need byte ranges or browsers can't seek (the scrubber snaps back)."""

    def test_range_request_is_partial(self):
        r = self.client.get("/video/1_1.mp4", HTTP_RANGE="bytes=100-199")
        self.assertEqual(r.status_code, 206)
        self.assertEqual(len(r.content), 100)
        self.assertTrue(r["Content-Range"].startswith("bytes 100-199/"))
        self.assertEqual(r["Accept-Ranges"], "bytes")

    def test_full_request_and_bad_names(self):
        r = self.client.get("/video/1_1.vtt")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Accept-Ranges"], "bytes")
        self.assertEqual(self.client.get("/video/..%2Fsettings.py").status_code, 404)
        self.assertEqual(self.client.get("/video/nope.mp4").status_code, 404)

    def test_lesson_nav_links_neighbours(self):
        r = self.client.get("/topic/1.2/")
        self.assertContains(r, 'href="/topic/1.1/"')
        self.assertContains(r, 'href="/topic/1.3/"')
        self.assertContains(r, "#unit-1")


class PaperTests(Assessments):
    """Solo students may print a unit test and its solutions manual; class students never get the manual."""

    def test_solo_student_gets_print_links_and_key(self):
        self.client.force_login(self.student("sol", in_class=False))
        r = self.client.get("/unit/U1/test/")
        forms = r.context["state_json"]["print"]["forms"]
        self.assertTrue(forms)
        r = self.client.get(forms[0]["key"])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/pdf")

    def test_class_student_gets_no_key(self):
        self.client.force_login(self.student("cal"))
        r = self.client.get("/unit/U1/test/")
        self.assertNotIn("print", r.context["state_json"])
        self.assertEqual(self.client.get("/unit/U1/test/print/A/key/").status_code, 403)


class Handouts(Assessments):
    def test_teacher_sees_every_pdf_and_students_cannot(self):
        self.client.force_login(self.teacher)
        r = self.client.get("/teacher/handouts/")
        self.assertContains(r, "/teacher/handouts/1.1/1.1-notes-key-classic.pdf")
        self.assertContains(r, "/teacher/handouts/U1/U1-unittest-formA-classic.pdf")
        pdf = self.client.get("/teacher/handouts/1.1/1.1-notes-classic.pdf")
        self.assertEqual(pdf["Content-Type"], "application/pdf")
        self.client.force_login(self.student("stu", in_class=False))
        self.assertEqual(self.client.get("/teacher/handouts/").status_code, 403)
        self.assertEqual(self.client.get("/teacher/handouts/1.1/1.1-notes-key-classic.pdf").status_code, 403)


class Packets(Assessments):
    """Lesson + practice + test prep in one PDF, stamped per download with the student's name and a traceable ID."""

    def setUp(self):
        super().setUp()
        import tempfile
        from pathlib import Path
        from unittest import mock

        import pymupdf
        from . import packets, views
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "1.1").mkdir()
        for name in ("1.1-packet-classic.pdf", "1.1-packet-key-classic.pdf"):
            doc = pymupdf.open()
            for i in range(3):
                doc.new_page(width=612, height=792).insert_text((72, 100), f"base page {i + 1}")
            doc.save(root / "1.1" / name)
        for patch in (mock.patch.object(packets, "PDF_DIR", root), mock.patch.object(views, "PDF_DIR", root)):
            patch.start()
            self.addCleanup(patch.stop)

    def download(self, num="1.1"):
        return self.client.post(f"/topic/{num}/packet/")

    def test_lesson_page_offers_the_packet(self):
        self.client.force_login(self.student("ana"))
        self.assertContains(self.client.get("/topic/1.1/"), 'action="/topic/1.1/packet/"')
        self.assertNotContains(self.client.get("/topic/1.2/"), "/packet/")      # no base PDF for 1.2 here

    def test_download_is_stamped_and_recorded(self):
        import pymupdf
        from .models import IssuedPacket
        self.client.force_login(self.student("ana"))
        r = self.download()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/pdf")
        p = IssuedPacket.objects.get()
        self.assertEqual((p.user.username, p.topic), ("ana", "1.1"))
        self.assertRegex(p.code, r"^[A-HJ-NP-Z2-9]{4}-[A-HJ-NP-Z2-9]{4}$")
        self.assertIn(p.code, r["Content-Disposition"])
        doc = pymupdf.open(stream=r.content, filetype="pdf")
        self.assertEqual(len(doc), 3)
        for page in doc:                                 # every page carries the name and the ID
            text = page.get_text()
            self.assertIn("Packet printed for Ana", text)
            self.assertIn(f"Packet ID {p.code}", text)
            self.assertIn("base page", text)
        self.download()
        self.assertEqual(len(set(IssuedPacket.objects.values_list("code", flat=True))), 2)   # one ID per download

    def test_only_members_by_post(self):
        self.assertEqual(self.download().status_code, 302)                       # visitors go to the login page
        self.client.force_login(self.student("ana"))
        self.assertEqual(self.client.get("/topic/1.1/packet/").status_code, 405)
        self.assertEqual(self.download("1.2").status_code, 404)
        nobody = User.objects.create_user("nob", password="pw123456")
        Profile.objects.create(user=nobody, display_name="Nob")
        self.client.force_login(nobody)
        self.assertEqual(self.download().status_code, 403)

    def test_teacher_gets_masters_and_traces_codes(self):
        from .models import IssuedPacket
        self.client.force_login(self.student("ana"))
        self.download()
        code = IssuedPacket.objects.get().code
        self.client.force_login(self.teacher)
        r = self.client.get("/teacher/handouts/")
        self.assertContains(r, "/teacher/handouts/1.1/1.1-packet-classic.pdf")
        self.assertContains(r, "/teacher/handouts/1.1/1.1-packet-key-classic.pdf")
        import pymupdf
        r = self.client.get("/teacher/handouts/1.1/1.1-packet-classic.pdf")       # the teacher's copy is stamped too
        mine = IssuedPacket.objects.filter(user=self.teacher).get()
        text = pymupdf.open(stream=r.content).load_page(0).get_text()
        self.assertIn(f"Printed for {packets.holder_name(self.teacher)}", text)
        self.assertIn(f"ID {mine.code}", text)
        r = self.client.get("/teacher/handouts/", {"packet": code.lower().replace("-", "")})
        self.assertEqual(r.context["lookup"]["found"]["username"], "ana")
        self.assertContains(r, "was printed by <strong>Ana</strong>")
        other = User.objects.create_user("other", password="pw123456")
        Profile.objects.create(user=other, role="teacher", display_name="Mr. Other")
        self.client.force_login(other)
        r = self.client.get("/teacher/handouts/", {"packet": code})
        self.assertIsNone(r.context["lookup"]["found"])          # not one of their students


class PrintedDocs(TestCase):
    """The LaTeX the build compiles: no answer lines for students, keys put the answer under the solution,
    unit tests number FRQs without titles and spell out the scoring."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        import importlib
        import sys
        from django.conf import settings
        sys.path.insert(0, str(settings.BASE_DIR.parent))
        cls.latex = importlib.import_module("calclib.latex")
        cls.topic = importlib.import_module("content.topic_1_1").TOPIC
        cls.test = importlib.import_module("content.unit_1").TEST

    def test_answer_line_is_key_only_and_flush_left(self):
        import os
        with open(os.path.join(self.latex.ROOT, "pdf", "calc.sty")) as f:
            line = next(l for l in f if l.startswith(r"\newcommand{\answerline}"))
        self.assertIn(r"\ifkey", line)
        self.assertNotIn(r"\hfill", line)
        self.assertIn(r"\begin{keepitem}", self.latex.practice_tex(self.topic, False, "classic"))

    def test_packet_has_all_three_parts(self):
        tex = self.latex.packet_tex(self.topic, False, "classic")
        for part in ("{Guided Notes}", "{Practice}", "{AP Test Prep}"):
            self.assertIn(part, tex)
        self.assertEqual(tex.count(r"\begin{document}"), 1)

    def test_unit_test_hides_frq_titles_and_states_scoring(self):
        from calclib import form
        student = self.latex.unittest_tex(self.test, False, "classic")
        key = self.latex.unittest_tex(self.test, True, "classic")
        frqs = form(self.test.frq, 0)
        for n, f in enumerate(frqs, 1):
            self.assertNotIn(f.title, student)
            self.assertIn(f"Question {n}", student)
            self.assertIn(f.title, key)
        total = len(form(self.test.mcq_a, 0)) + len(form(self.test.mcq_b, 0)) + sum(f.points for f in frqs)
        self.assertIn(f"Total: {total} points", student)
        self.assertIn("1 point each", student)
        for f in content.public("U1")["frq"]:                 # the web test doesn't name them either
            self.assertRegex(f["title"], r"^Question \d+$")
            self.assertNotIn("type", f)
