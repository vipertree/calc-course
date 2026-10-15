import json
import json
import re

from django.contrib.auth.models import User
from django.test import Client, TestCase

from accounts.antibot import stamp
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

    def test_antiderivatives_need_plus_c(self):
        spec = {"kind": "expr", "value": "x**3/3 - 2*x + 5*log(abs(x)) + C", "var": "x"}
        for g in ("x^3/3-2x+5ln|x|+C", r"x^3/3-2x+5\ln|x|+C", "x^3/3-2x+5ln|x|+7+C", "x^3/3 - 2x + 5ln(x) + C"):
            self.assertTrue(grading.check(g, spec), g)
        self.assertFalse(grading.check("x^3/3-2x+5ln|x|", spec))     # no + C
        self.assertFalse(grading.check("x^3/3+C", spec))

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
                                           "password": "slope-field-42", "started": stamp(10)})

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

    def test_visitor_free_lesson(self):
        """Units 1-3 are free (Adder 2026-10-08): a visitor gets the whole lesson and can check any answer, but
        nothing is saved, and taking a unit test needs a free account."""
        r = self.client.get("/topic/2.1/")
        self.assertEqual(r.status_code, 200)
        body = r.content.decode()
        self.assertNotIn('"preview": true', body)
        self.assertIn("Shrinking the interval", body)               # the notes are there
        self.assertIn("Make a free account", body)
        ok = self.client.post("/api/2.1/check/", json.dumps({"item": "p2_1-1", "given": "11", "area": "practice"}),
                              content_type="application/json")
        self.assertTrue(ok.json()["correct"])
        later = self.client.post("/api/2.1/check/", json.dumps({"item": "p2_1-6", "given": "1", "area": "practice"}),
                                 content_type="application/json")
        self.assertEqual(later.status_code, 200)                     # every practice problem, not just the first few
        self.assertEqual(Response.objects.count(), 0)                # nothing saved for visitors
        self.assertEqual(self.client.get("/unit/U1/test/").status_code, 302)   # to sign-up

    def test_visitor_preview(self):
        """Unit 4 on is for members: a visitor gets the video and the first few practice problems."""
        r = self.client.get("/topic/4.1/")
        self.assertEqual(r.status_code, 200)
        self.assertIn('"preview": true', r.content.decode())
        no = self.client.post("/api/4.1/check/", json.dumps({"item": "p4_1-6", "given": "1", "area": "practice"}),
                              content_type="application/json")
        self.assertEqual(no.status_code, 403)
        self.assertContains(self.client.get("/unit/U4/test/"), "for members")
        self.assertEqual(self.client.get("/course/").status_code, 200)

    def test_student_cannot_see_dashboard(self):
        self.join()
        self.assertEqual(self.client.get("/teacher/").status_code, 403)


class Designs(TestCase):
    def test_safety_card_is_the_only_design(self):
        """Adder 2026-10-15: Safety card everywhere; the Design menu and the other looks are mothballed."""
        page = self.client.get("/course/").content.decode()
        self.assertIn('data-design="safety"', page)
        self.assertIn("css/designs/safety.css", page)
        self.assertNotIn("design-pick", page)
        self.assertEqual(self.client.get("/design/transit/?next=/course/").status_code, 404)
        self.client.cookies["design"] = "transit"
        self.assertIn('data-design="safety"', self.client.get("/course/").content.decode())

    def test_theme_switch(self):
        page = self.client.get("/course/").content.decode()
        self.assertIn('class="theme-switch" role="switch"', page)
        self.client.get("/theme/slate/?next=/course/")
        self.assertIn('data-theme="slate"', self.client.get("/course/").content.decode())

    def test_transit_map_columns(self):
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


class Drafts(Assessments):
    """Answer boxes keep what was typed across a reload; blanks already right come back from the answer key."""

    def state(self, url="/topic/1.1/"):
        r = self.client.get(url)
        m = re.search(r'<script id="state" type="application/json">(.*?)</script>', r.content.decode(), re.S)
        return json.loads(m.group(1))

    def test_drafts_round_trip_and_correct_blanks_autofill(self):
        u = self.student("dee", in_class=False)
        self.client.force_login(u)
        post = lambda body: self.client.post("/api/1.1/draft/", json.dumps(body), content_type="application/json")
        self.assertEqual(post({"item": "n1_1-b1", "value": "a guess"}).status_code, 200)
        self.assertEqual(post({"item": "n1_1-b1", "value": "a better guess"}).status_code, 200)   # one row per box
        post({"item": "n1_1-b6", "value": "", "revealed": True})
        self.client.post("/api/1.1/check/", json.dumps({"item": "n1_1-b2", "given": "time", "area": "notes"}),
                         content_type="application/json")
        st = self.state()
        self.assertEqual(st["drafts"]["n1_1-b1"]["v"], "a better guess")
        self.assertEqual(st["shown"]["n1_1-b2"], "time")                    # right before: filled from the key
        self.assertEqual(st["shown"]["n1_1-b6"], "undefined")               # shown on request: stays shown
        self.assertNotIn("n1_1-b1", st["shown"])                             # never right: no answer leaks
        other = self.student("eve", in_class=False)
        self.client.force_login(other)
        self.assertEqual(self.state()["drafts"], {})                         # drafts are per student

    def test_visitors_cannot_save_drafts(self):
        self.assertEqual(self.client.post("/api/1.1/draft/", "{}", content_type="application/json").status_code, 302)
        nob = self.student("nob", in_class=False)
        nob.profile.full_access = False; nob.profile.save()
        self.client.force_login(nob)
        r = self.client.post("/api/4.1/draft/", json.dumps({"item": "x", "value": "y"}), content_type="application/json")
        self.assertEqual(r.status_code, 403)                         # a paid unit
        r = self.client.post("/api/1.1/draft/", json.dumps({"item": "x", "value": "y"}), content_type="application/json")
        self.assertNotEqual(r.status_code, 403)                      # a free unit saves for a free account


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
        self.assertEqual(self.download("4.1").status_code, 403)                  # a paid unit
        self.assertNotEqual(self.download().status_code, 403)                    # Unit 1 prints with a free account

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
            self.assertNotIn(f.title, key)                    # no titles anywhere, keys included
        for f in self.topic.frq:                              # nor in test prep, on paper or on the web
            self.assertNotIn(f.title, self.latex.testprep_tex(self.topic, False, "classic"))
            self.assertNotIn(f.title, self.latex.testprep_tex(self.topic, True, "classic"))
            self.assertNotIn(f.title, json.dumps(content.public("1.1")))
        total = len(form(self.test.mcq_a, 0)) + len(form(self.test.mcq_b, 0)) + sum(f.points for f in frqs)
        self.assertIn(f"Total: {total} points", student)
        self.assertIn("1 point each", student)
        for f in content.public("U1")["frq"]:                 # the web test doesn't name them either
            self.assertRegex(f["title"], r"^Question \d+$")
            self.assertNotIn("type", f)


class SlideDecks(Assessments):
    """Teacher slide decks (tools/build_slides.py): every page and file is for teacher accounts only."""

    def setUp(self):
        super().setUp()
        import tempfile
        from pathlib import Path
        from django.test import override_settings
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        d = Path(self.tmp.name) / "1.2"
        (d / "clips").mkdir(parents=True)
        (d / "manifest.json").write_text(json.dumps({"topic": "1.2", "title": "Limits", "versions": {
            "solutions": {"html": "deck-solutions.html", "slides": 30, "clips": 6, "pptx": "1.2-slides-solutions.pptx"},
            "blank": {"html": "deck-blank.html", "slides": 25, "clips": 6, "pptx": "1.2-slides-blank.pptx"}}}))
        for v in ("solutions", "blank"):
            (d / f"deck-{v}.html").write_text(f'<!doctype html><html lang="en"><body>{v} deck<div class="ver"><!--slides-for--></div></body></html>')
            (d / f"1.2-slides-{v}.pptx").write_bytes(b"PK\x03\x04 not really a deck")
        (d / "clips" / "ex1-full.mp4").write_bytes(bytes(range(256)) * 4)
        (d / "clips" / "ex1-full.jpg").write_bytes(b"\xff\xd8\xff jpeg")
        (d / "notes.txt").write_text("not something a deck folder hands out")
        o = override_settings(SLIDES_DIR=Path(self.tmp.name), SLIDES_ACCEL="")
        o.enable()
        self.addCleanup(o.disable)

    URLS = ["/teacher/slides/1.2/", "/teacher/slides/1.2/deck-solutions.html", "/teacher/slides/1.2/deck-blank.html",
            "/teacher/slides/1.2/1.2-slides-solutions.pptx", "/teacher/slides/1.2/1.2-slides-blank.pptx",
            "/teacher/slides/1.2/clips/ex1-full.mp4", "/teacher/slides/1.2/clips/ex1-full.jpg"]

    def test_teacher_gets_page_decks_pptx_and_clips(self):
        self.client.force_login(self.teacher)
        r = self.client.get("/teacher/slides/1.2/")
        self.assertEqual(r.status_code, 200)
        for u in self.URLS[1:5]:
            self.assertContains(r, f'href="{u}"')
        r = self.client.get("/teacher/slides/1.2/deck-solutions.html")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "solutions deck")
        self.assertContains(r, "Prepared for Ms. Teach")
        r = self.client.get("/teacher/slides/1.2/1.2-slides-blank.pptx")
        self.assertEqual(r.status_code, 200)
        self.assertIn("attachment", r["Content-Disposition"])
        self.assertTrue(r["Content-Type"].startswith("application/vnd.openxmlformats-officedocument.presentationml"))
        r = self.client.get("/teacher/slides/1.2/clips/ex1-full.mp4", HTTP_RANGE="bytes=0-99")
        self.assertEqual(r.status_code, 206)                     # seekable
        self.assertEqual(len(r.content), 100)
        self.assertEqual(self.client.get("/teacher/slides/1.2/clips/ex1-full.jpg")["Content-Type"], "image/jpeg")

    def test_deck_opens_in_the_sites_look(self):
        self.client.force_login(self.teacher)
        self.client.cookies["theme"] = "slate"
        self.assertContains(self.client.get("/teacher/slides/1.2/deck-blank.html"), '<html lang="en" data-theme="slate">')
        self.client.cookies["theme"] = "bogus"
        self.assertContains(self.client.get("/teacher/slides/1.2/deck-blank.html"), '<html lang="en">')

    def test_students_and_visitors_get_403_everywhere(self):
        for who in (self.student("solo", in_class=False), self.student("classy"), None):
            c = Client()
            if who is not None:
                c.force_login(who)
            for u in self.URLS:
                self.assertEqual(c.get(u).status_code, 403, (who, u))
            self.assertEqual(c.get("/teacher/slides/1.2/clips/ex1-full.mp4", HTTP_RANGE="bytes=0-99").status_code, 403)

    def test_only_deck_files_are_served(self):
        self.client.force_login(self.teacher)
        for name in ("manifest.json", "notes.txt", "deck-other.html", "clips/nope.mp4", "..%2Fmanifest.json",
                     "1.3-slides-blank.pptx"):
            self.assertEqual(self.client.get(f"/teacher/slides/1.2/{name}").status_code, 404, name)
        self.assertEqual(self.client.get("/teacher/slides/1.4/").status_code, 404)      # no deck built

    def test_production_hands_files_to_nginx_after_the_check(self):
        from django.test import override_settings
        with override_settings(SLIDES_ACCEL="/protected-slides/"):
            self.client.force_login(self.teacher)
            r = self.client.get("/teacher/slides/1.2/clips/ex1-full.mp4")
            self.assertEqual(r["X-Accel-Redirect"], "/protected-slides/1.2/clips/ex1-full.mp4")
            self.assertEqual(r.content, b"")
            r = self.client.get("/teacher/slides/1.2/1.2-slides-solutions.pptx")
            self.assertEqual(r["X-Accel-Redirect"], "/protected-slides/1.2/1.2-slides-solutions.pptx")
            self.assertIn("attachment", r["Content-Disposition"])
            self.client.force_login(self.student("stu", in_class=False))
            r = self.client.get("/teacher/slides/1.2/clips/ex1-full.mp4")
            self.assertEqual(r.status_code, 403)
            self.assertNotIn("X-Accel-Redirect", r)

    def test_slides_link_only_for_teachers(self):
        self.client.force_login(self.teacher)
        self.assertContains(self.client.get("/teacher/handouts/"), 'href="/teacher/slides/1.2/"')
        self.assertContains(self.client.get("/topic/1.2/"), 'href="/teacher/slides/1.2/"')
        self.assertNotContains(self.client.get("/topic/1.1/"), "/teacher/slides/")      # 1.1 has no deck here
        self.client.force_login(self.student("stu", in_class=False))
        self.assertNotContains(self.client.get("/topic/1.2/"), "/teacher/slides/")


class SitePages(TestCase):
    """The landing page sorts visitors into students and teachers; membership checkout is a placeholder until
    Stripe is connected (course/payments.py)."""

    def test_landing_for_visitors(self):
        page = self.client.get("/").content.decode()
        self.assertIn('href="/students/"', page)
        self.assertIn('href="/teachers/"', page)
        self.assertIn("A lot of it is free", page)
        for url in ("/students/", "/teachers/", "/membership/"):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_signed_in_students_skip_the_landing(self):
        u = User.objects.create_user("kim", password="pw123456")
        Profile.objects.create(user=u, display_name="Kim")
        self.client.force_login(u)
        self.assertNotIn("A lot of it is free", self.client.get("/").content.decode())

    def test_checkout_is_a_placeholder(self):
        r = self.client.get("/membership/student/")
        self.assertContains(r, "isn't open yet")
        self.assertEqual(self.client.get("/membership/nonsense/").status_code, 404)

    def test_course_flyouts(self):
        """Adder 2026-10-15: hover AP Calc Course for its units, a unit for its lessons; Trig Course lists its lessons."""
        page = self.client.get("/videos/").content.decode()
        self.assertIn('href="/course/#unit-6" aria-haspopup="true"', page)
        self.assertIn('href="/topic/6.4/"', page)                      # a lesson, two levels down
        self.assertIn('href="/unit/U1/test/"', page)
        self.assertIn("Right-Triangle Trigonometry", page)             # the trig lessons under Trig Course
        self.assertIn('Unit 4</b><span>Contextual Applications of Differentiation <i class="lock">Members</i>', page)
        self.assertNotIn('Unit 1</b><span>Limits and Continuity <i class="lock">', page)

    def test_videos_menu(self):
        """Adder 2026-10-15: the Videos dropdown lists each unit with a flyout of its published videos."""
        import tempfile
        from pathlib import Path
        from django.test import override_settings
        with tempfile.TemporaryDirectory() as d:
            for name in ("2_1.mp4", "2_1-dark.mp4", "0_1.mp4"):
                (Path(d) / name).write_bytes(b"")
            with override_settings(VIDEO_DIR=Path(d)):
                page = self.client.get("/course/").content.decode()
        self.assertIn('href="/videos/#2.1"><b>2.1</b>', page)
        self.assertIn('href="/videos/#0.1"', page)
        self.assertNotIn('href="/videos/#2.2"', page)                  # no video, no entry
        self.assertNotIn('href="/videos/#1.1"', page)                  # nor a unit with none

    def test_new_navigation_pages(self):
        """Adder 2026-10-12: separate calc and trig courses and formula sheets, an all-videos page, a student
        dashboard, and a top bar in two layouts."""
        calc = self.client.get("/course/").content.decode()
        self.assertIn("AP Calc Course", calc)
        self.assertNotIn('<details class="unit module"', calc)          # the trig module has its own page now
        self.assertIn('<details class="unit module"', self.client.get("/trig/").content.decode())
        self.assertContains(self.client.get("/trig/formulas/"), "Trig Formulas")
        self.assertContains(self.client.get("/formulas/"), "Calc Formula Sheet")
        self.assertEqual(self.client.get("/videos/").status_code, 200)
        self.assertEqual(self.client.get("/me/").status_code, 302)       # sign in first
        self.assertIn("Mr Oaks Math", calc)
        self.assertNotIn(">Free<", calc)
        self.assertIn('class="nav-group', calc)                         # dropdowns, no layout choice any more
        self.assertEqual(self.client.get("/nav/links/?next=/course/").status_code, 404)
        u = User.objects.create_user("lee", password="pw123456")
        Profile.objects.create(user=u, display_name="Lee")
        self.client.force_login(u)
        self.assertRedirects(self.client.get("/"), "/me/")
        self.assertContains(self.client.get("/me/"), "Student Dashboard")


class UnitEndNext(TestCase):
    """Adder 2026-10-14: Next at the end of a unit goes to that unit's test, not the next unit's first lesson."""

    def test_last_lesson_points_to_the_unit_test(self):
        from . import content
        last = [t["n"] for u in content.syllabus() if u["n"] == 1 for t in u["topics"] if t["n"] in content.available()][-1]
        page = self.client.get(f"/topic/{last}/").content.decode().split("</header>", 1)[1]   # not the top-bar flyouts
        self.assertIn('href="/unit/U1/test/"', page)
        self.assertNotIn('href="/topic/2.1/"', page)
