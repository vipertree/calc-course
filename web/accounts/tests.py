import json
import os
import re
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail, signing
from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from course.models import Draft, QuizAttempt, Response, StepDone

from . import views
from .antibot import stamp
from .models import Classroom, Enrollment, Profile

PW = "slope-field-42"
WEB = Path(settings.BASE_DIR)


def make_user(username, role="student", email="", verified=False, password=PW, name=None):
    u = User.objects.create_user(username, email=email, password=password)
    Profile.objects.create(user=u, role=role, display_name=name or username.title(), email_verified=verified)
    return u


def link_in(message):
    return re.search(r"https?://testserver(/\S+)", message.body).group(1)


class SignUp(TestCase):
    def form(self, **kw):
        d = {"display_name": "Kai Moreno", "email": "kai@example.com", "username": "kai", "password": PW,
             "age_ok": "on", "started": stamp(10)}
        d.update(kw)
        return d

    def test_signup_sends_a_link_that_confirms_the_email(self):
        r = self.client.post("/signup/", self.form())
        self.assertEqual(r.status_code, 302)
        u = User.objects.get(username="kai")
        self.assertFalse(u.profile.email_verified)
        self.assertEqual(u.profile.role, "student")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["kai@example.com"])
        r = self.client.get(link_in(mail.outbox[0]))
        self.assertContains(r, "Email confirmed")
        u.profile.refresh_from_db()
        self.assertTrue(u.profile.email_verified)

    def test_bots_are_turned_away(self):
        for bad in ({"website": "http://spam.example"}, {"started": stamp(0)}, {"started": "forged"},
                    {"started": stamp(2 * 86400)}, {"started": ""}):
            r = self.client.post("/signup/", self.form(**bad))
            self.assertEqual(r.status_code, 200, bad)
            self.assertContains(r, "Something went wrong with that form")
        self.assertFalse(User.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_must_be_13_and_use_a_real_password(self):
        r = self.client.post("/signup/", self.form(age_ok=""))
        self.assertContains(r, "13 or older")
        r = self.client.post("/signup/", self.form(password="password"))
        self.assertContains(r, "too common")
        self.assertFalse(User.objects.exists())

    def test_confirmed_email_cannot_be_reused(self):
        make_user("old", email="kai@example.com", verified=True)
        r = self.client.post("/signup/", self.form())
        self.assertContains(r, "already uses that email")

    def test_join_form_asks_for_no_email(self):
        t = make_user("teach", role="teacher")
        c = Classroom.objects.create(name="P3", teacher=t)
        page = self.client.get(f"/join/?code={c.code}").content.decode()
        self.assertNotIn('type="email"', page)
        self.assertIn('class="hp"', page)
        r = self.client.post("/join/", {"code": c.code, "display_name": "Ana R", "username": "ana", "password": PW,
                                        "website": "x", "started": stamp(10)})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username="ana").exists())

    def test_teacher_request_needs_approval_and_a_confirmed_email(self):
        r = self.client.post("/signup/teacher/", {"display_name": "Ms. Rivera", "email": "rivera@school.example",
                                                  "school": "Central High", "username": "rivera", "password": PW,
                                                  "started": stamp(10)})
        self.assertEqual(r.status_code, 302)
        p = Profile.objects.get(user__username="rivera")
        self.assertEqual(p.role, "student")                 # no answer keys until a person approves
        self.assertIsNotNone(p.teacher_requested)
        self.assertEqual(self.client.get("/teacher/").status_code, 403)
        self.assertContains(self.client.get("/course/"), "waiting for approval")
        from django.core.management.base import CommandError
        with self.assertRaises(CommandError):
            call_command("approve_teacher", "rivera")       # email not confirmed yet
        self.client.get(link_in(mail.outbox[0]))
        call_command("approve_teacher", "rivera")
        p.refresh_from_db()
        self.assertEqual(p.role, "teacher")
        self.assertEqual(self.client.get("/teacher/").status_code, 200)

    def test_teacher_cannot_join_a_class_as_a_student(self):
        t = make_user("teach", role="teacher")
        other = make_user("teach2", role="teacher")
        c = Classroom.objects.create(name="P3", teacher=other)
        self.client.force_login(t)
        self.client.post("/join/", {"code": c.code})
        self.assertFalse(Enrollment.objects.exists())


class EmailLinks(TestCase):
    def setUp(self):
        self.u = make_user("kai", email="kai@example.com")

    def test_old_links_die_when_the_email_changes(self):
        old = views.verify_token(self.u, "kai@example.com")
        self.u.email = "other@example.com"
        self.u.save()
        r = self.client.get(f"/verify/{old}/")
        self.assertEqual(r.status_code, 400)
        self.u.profile.refresh_from_db()
        self.assertFalse(self.u.profile.email_verified)

    def test_tampered_and_expired_links(self):
        self.assertEqual(self.client.get("/verify/nonsense/").status_code, 400)
        token = views.verify_token(self.u, "kai@example.com")
        with override_settings(EMAIL_VERIFY_DAYS=-1):
            r = self.client.get(f"/verify/{token}/")
        self.assertContains(r, "expired", status_code=400)

    def test_change_email_takes_effect_only_from_the_new_inbox(self):
        self.client.force_login(self.u)
        r = self.client.post("/account/email/", {"email": "new@example.com", "password": "wrong"})
        self.assertContains(r, "password isn&#x27;t right", status_code=400)
        self.client.post("/account/email/", {"email": "new@example.com", "password": PW})
        self.u.refresh_from_db()
        self.assertEqual(self.u.email, "kai@example.com")
        self.assertEqual(mail.outbox[-1].to, ["new@example.com"])
        self.client.get(link_in(mail.outbox[-1]))
        self.u.refresh_from_db()
        self.assertEqual(self.u.email, "new@example.com")
        self.assertTrue(self.u.profile.email_verified)


class SignIn(TestCase):
    def test_sign_in_with_confirmed_email_only(self):
        make_user("kai", email="kai@example.com", verified=True)
        make_user("lee", email="lee@example.com", verified=False)
        self.assertTrue(self.client.login(username="kai@example.com", password=PW))
        self.client.logout()
        self.assertFalse(self.client.login(username="lee@example.com", password=PW))
        self.assertTrue(self.client.login(username="lee", password=PW))

    @override_settings(RATELIMIT_ENABLED=True)
    def test_guessing_one_account_gets_slowed(self):
        cache.clear()
        make_user("kai")
        for _ in range(10):
            r = self.client.post("/login/", {"username": "kai", "password": "nope"})
            self.assertEqual(r.status_code, 200)
        r = self.client.post("/login/", {"username": "kai", "password": PW})
        self.assertEqual(r.status_code, 429)
        self.assertContains(r, "Too many tries", status_code=429)
        cache.clear()

    def test_login_page_links(self):
        r = self.client.get("/login/")
        for url in ("/password-reset/", "/join/", "/signup/", "/signup/teacher/"):
            self.assertContains(r, f'href="{url}"')


class PasswordReset(TestCase):
    def test_reset_by_email(self):
        u = make_user("kai", email="kai@example.com", verified=True)
        r = self.client.post("/password-reset/", {"email": "kai@example.com", "started": stamp(10)})
        self.assertRedirects(r, "/password-reset/sent/")
        self.assertEqual(len(mail.outbox), 1)
        link = link_in(mail.outbox[0])
        r = self.client.get(link, follow=True)
        self.assertContains(r, "Choose a new password")
        r = self.client.post(r.redirect_chain[-1][0], {"new_password1": "integral-curve-7",
                                                       "new_password2": "integral-curve-7"})
        self.assertRedirects(r, "/password-reset/done/")
        u.refresh_from_db()
        self.assertTrue(u.check_password("integral-curve-7"))

    def test_no_mail_to_unconfirmed_addresses_and_no_hint_either_way(self):
        make_user("kai", email="kai@example.com", verified=False)
        r = self.client.post("/password-reset/", {"email": "kai@example.com", "started": stamp(10)})
        self.assertRedirects(r, "/password-reset/sent/")
        r = self.client.post("/password-reset/", {"email": "nobody@example.com", "started": stamp(10)})
        self.assertRedirects(r, "/password-reset/sent/")
        self.assertEqual(len(mail.outbox), 0)

    def test_bot_check(self):
        make_user("kai", email="kai@example.com", verified=True)
        r = self.client.post("/password-reset/", {"email": "kai@example.com", "started": stamp(0)})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(RATELIMIT_ENABLED=True)
    def test_one_inbox_gets_at_most_three_an_hour(self):
        cache.clear()
        make_user("kai", email="kai@example.com", verified=True)
        for _ in range(6):
            self.client.post("/password-reset/", {"email": "kai@example.com", "started": stamp(10)})
        self.assertEqual(len(mail.outbox), 3)
        cache.clear()


class AccountSettings(TestCase):
    def setUp(self):
        self.t = make_user("teach", role="teacher", name="Ms. Teach")
        self.c = Classroom.objects.create(name="Period 3", teacher=self.t)
        self.u = make_user("ana", name="Ana R")
        Enrollment.objects.create(classroom=self.c, student=self.u)
        self.client.force_login(self.u)

    def test_page_renders_for_everyone(self):
        self.assertContains(self.client.get("/account/"), "Account settings")
        admin = User.objects.create_superuser("root", password=PW)     # no profile: one is made
        self.client.force_login(admin)
        self.assertContains(self.client.get("/account/"), "Account settings")

    def test_change_name_and_password(self):
        self.client.post("/account/name/", {"display_name": "  Ana   Ruiz "})
        self.u.profile.refresh_from_db()
        self.assertEqual(self.u.profile.display_name, "Ana Ruiz")
        r = self.client.post("/account/password/", {"old_password": PW, "new_password1": "tangent-line-9",
                                                    "new_password2": "tangent-line-9"})
        self.assertRedirects(r, "/account/")
        self.u.refresh_from_db()
        self.assertTrue(self.u.check_password("tangent-line-9"))
        self.assertEqual(self.client.get("/account/").status_code, 200)     # still signed in

    def test_export_has_my_data_and_nobody_elses(self):
        other = make_user("ben")
        Response.objects.create(user=self.u, topic="2.1", item="p2_1-1", area="practice", given="mine-11", correct=True)
        Response.objects.create(user=other, topic="2.1", item="p2_1-1", area="practice", given="theirs-12", correct=False)
        Draft.objects.create(user=self.u, topic="2.1", item="x", value="my draft")
        Draft.objects.create(user=other, topic="2.1", item="x", value="their draft")
        StepDone.objects.create(user=self.u, topic="2.1", step=0)
        r = self.client.get("/account/export/")
        self.assertEqual(r["Content-Type"], "application/json")
        self.assertIn("attachment", r["Content-Disposition"])
        d = json.loads(r.content)
        self.assertEqual(d["account"]["username"], "ana")
        self.assertEqual(d["classes_joined"][0]["class"], "Period 3")
        body = r.content.decode()
        self.assertIn("mine-11", body)
        self.assertIn("my draft", body)
        self.assertNotIn("theirs-12", body)
        self.assertNotIn("their draft", body)
        self.assertNotIn("pbkdf2", body)                        # no password hash

    def test_delete_needs_password_and_removes_everything(self):
        Response.objects.create(user=self.u, topic="2.1", item="a", area="practice", given="1", correct=True)
        r = self.client.post("/account/delete/", {"password": "wrong", "sure": "on"})
        self.assertContains(r, "password isn&#x27;t right", status_code=400)
        r = self.client.post("/account/delete/", {"password": PW})
        self.assertEqual(r.status_code, 400)                     # the box must be ticked
        self.assertTrue(User.objects.filter(username="ana").exists())
        r = self.client.post("/account/delete/", {"password": PW, "sure": "on"})
        self.assertContains(r, "Your account is deleted")
        self.assertFalse(User.objects.filter(username="ana").exists())
        self.assertFalse(Response.objects.exists())
        self.assertFalse(Enrollment.objects.exists())
        self.assertEqual(self.client.get("/account/").status_code, 302)       # signed out

    def test_teacher_delete_takes_classes_but_not_students(self):
        QuizAttempt.objects.create(user=self.u, topic="2.1", score=1, total=2, classroom=self.c)
        self.client.force_login(self.t)
        self.assertContains(self.client.get("/account/"), "Your classes are deleted too")
        self.client.post("/account/delete/", {"password": PW, "sure": "on"})
        self.assertFalse(Classroom.objects.exists())
        self.assertTrue(User.objects.filter(username="ana").exists())
        self.assertEqual(QuizAttempt.objects.get().classroom, None)

    def test_leave_class(self):
        self.client.post(f"/account/leave/{self.c.pk}/")
        self.assertFalse(Enrollment.objects.exists())

    def test_purge_unverified(self):
        stale = make_user("stale", email="s@example.com")
        User.objects.filter(pk=stale.pk).update(date_joined=timezone.now() - timedelta(days=30))
        busy = make_user("busy", email="b@example.com")
        User.objects.filter(pk=busy.pk).update(date_joined=timezone.now() - timedelta(days=30))
        StepDone.objects.create(user=busy, topic="1.1", step=0)
        fresh = make_user("fresh", email="f@example.com")
        call_command("purge_unverified", stdout=open(os.devnull, "w"))
        names = set(User.objects.values_list("username", flat=True))
        self.assertNotIn("stale", names)
        self.assertTrue({"busy", "fresh", "ana", "teach"} <= names)    # class students have no email at all


class TeacherOnly(TestCase):
    """Every teacher view checks the role, and teachers reach only their own classes and students."""

    def setUp(self):
        self.t = make_user("teach", role="teacher", name="Ms. Teach")
        self.c = Classroom.objects.create(name="Period 3", teacher=self.t)
        self.t2 = make_user("teach2", role="teacher")
        self.c2 = Classroom.objects.create(name="Other", teacher=self.t2)
        self.s = make_user("ana", name="Ana R")
        Enrollment.objects.create(classroom=self.c, student=self.s)
        self.s2 = make_user("ben")
        Enrollment.objects.create(classroom=self.c2, student=self.s2)

    def urls(self):
        c, s = self.c.pk, self.s.pk
        return [("get", "/teacher/"), ("get", "/teacher/transcripts/"), ("get", "/teacher/handouts/"),
                ("get", "/teacher/handouts/1.1/1.1-notes-key-classic.pdf"),
                ("post", "/teacher/class/new/"), ("post", f"/teacher/class/{c}/toggle/"),
                ("post", f"/teacher/class/{c}/release/1.1/"),
                ("post", f"/teacher/class/{c}/student/{s}/reset-password/"),
                ("post", f"/teacher/class/{c}/student/{s}/remove/")]

    def test_students_get_403_and_visitors_sign_in(self):
        for method, url in self.urls():
            r = getattr(self.client, method)(url)
            self.assertEqual(r.status_code, 302, url)
            self.assertIn("/login/", r["Location"])
        self.client.force_login(self.s)
        for method, url in self.urls():
            self.assertEqual(getattr(self.client, method)(url).status_code, 403, url)
        self.client.force_login(self.t2)          # a teacher, but not this class's
        for method, url in self.urls()[5:]:
            self.assertEqual(getattr(self.client, method)(url).status_code, 404, url)
        self.assertTrue(Enrollment.objects.filter(student=self.s).exists())
        self.assertTrue(self.s.check_password(PW))

    def test_reset_student_password_shows_it_once(self):
        self.client.force_login(self.t)
        r = self.client.post(f"/teacher/class/{self.c.pk}/student/{self.s.pk}/reset-password/", follow=True)
        pw = re.search(r'<span class="code">([a-z0-9-]{14})</span>', r.content.decode()).group(1)
        self.s.refresh_from_db()
        self.assertTrue(self.s.check_password(pw))
        self.assertNotIn(pw, self.client.get("/teacher/").content.decode())
        self.assertNotIn(pw, " ".join(f"{k}={v.value}" for k, v in self.client.cookies.items()))

    def test_teacher_cannot_reset_a_student_outside_their_classes_or_a_teacher(self):
        self.client.force_login(self.t)
        url = f"/teacher/class/{self.c.pk}/student/{self.s2.pk}/reset-password/"
        self.assertEqual(self.client.post(url).status_code, 404)
        Enrollment.objects.create(classroom=self.c, student=self.t2)        # a teacher somehow in the roster
        url = f"/teacher/class/{self.c.pk}/student/{self.t2.pk}/reset-password/"
        self.assertEqual(self.client.post(url).status_code, 404)
        self.t2.refresh_from_db()
        self.assertTrue(self.t2.check_password(PW))

    def test_remove_student(self):
        self.client.force_login(self.t)
        self.client.post(f"/teacher/class/{self.c.pk}/student/{self.s.pk}/remove/")
        self.assertFalse(Enrollment.objects.filter(student=self.s).exists())
        self.assertTrue(User.objects.filter(pk=self.s.pk).exists())

    def test_new_class_course_is_checked(self):
        self.client.force_login(self.t)
        self.client.post("/teacher/class/new/", {"name": "P5", "course": "<script>"})
        self.assertEqual(Classroom.objects.get(name="P5").course, "AB")

    def test_dashboard_shows_only_my_students(self):
        self.client.force_login(self.t)
        r = self.client.get("/teacher/")
        self.assertContains(r, "Ana R")
        self.assertNotContains(r, "Ben")


class ApiHardening(TestCase):
    """Malformed posts get a 4xx, never a 500, and nobody reaches another student's work."""

    def setUp(self):
        t = make_user("teach", role="teacher")
        self.c = Classroom.objects.create(name="P3", teacher=t)
        self.a, self.b = make_user("ana"), make_user("ben")
        for u in (self.a, self.b):
            Enrollment.objects.create(classroom=self.c, student=u)

    def post(self, url, body):
        return self.client.post(url, body if isinstance(body, str) else json.dumps(body), content_type="application/json")

    def test_garbage_bodies(self):
        self.client.force_login(self.a)
        bodies = ["[1,2]", "42", "not json", {"item": ["x"]}, {"item": {"a": 1}, "given": ["x"]},
                  {"item": "p2_1-1", "given": 11}, {"item": "p2_1-1", "given": None, "area": 5},
                  {"step": "x"}, {"step": None}, {"part": ["f2_1-1a"], "earned": "lots"},
                  {"part": "f2_1-1a", "earned": "lots"}, {"answers": [1, 2]}, {"answers": {"x": {"y": 1}}},
                  {"item": "z" * 5000, "value": {"nested": True}}]
        for api in ("check", "step", "draft", "quiz", "frq"):
            for body in bodies:
                r = self.post(f"/api/2.1/{api}/", body)
                self.assertLess(r.status_code, 500, f"{api} {body}")
                self.assertGreaterEqual(r.status_code, 200)

    def test_get_is_refused(self):
        self.client.force_login(self.a)
        for api in ("check", "step", "draft", "quiz", "frq"):
            self.assertEqual(self.client.get(f"/api/2.1/{api}/").status_code, 405)

    def test_csrf_is_enforced(self):
        from django.test import Client
        c = Client(enforce_csrf_checks=True)
        c.force_login(self.a)
        r = c.post("/api/2.1/draft/", json.dumps({"item": "x", "value": "1"}), content_type="application/json")
        self.assertEqual(r.status_code, 403)

    def test_drafts_stay_private(self):
        self.client.force_login(self.b)
        self.post("/api/2.1/draft/", {"item": "n2_1-b3", "value": "bens-secret-draft"})
        self.client.force_login(self.a)
        self.post("/api/2.1/draft/", {"item": "n2_1-b3", "value": "anas-draft"})
        page = self.client.get("/topic/2.1/").content.decode()
        self.assertIn("anas-draft", page)
        self.assertNotIn("bens-secret-draft", page)
        self.assertEqual(Draft.objects.get(user=self.b).value, "bens-secret-draft")   # untouched

    @override_settings(RATELIMIT_ENABLED=True)
    def test_answer_checks_are_rate_limited(self):
        cache.clear()
        self.client.force_login(self.a)
        codes = [self.post("/api/2.1/check/", {"item": "p2_1-1", "given": "1", "area": "practice"}).status_code
                 for _ in range(301)]
        self.assertEqual(codes[:300], [200] * 300)
        self.assertEqual(codes[300], 429)
        r = self.post("/api/2.1/check/", {"item": "p2_1-1", "given": "1", "area": "practice"})
        self.assertIn("too many", r.json()["error"])
        cache.clear()


class ExamsAndSlides(TestCase):
    """Views added on main after this review began: practice exams (per-student attempts) and teacher slides."""

    def setUp(self):
        from course import exams
        self.exams = exams
        self.slug = "ab1"
        if not exams.public(self.slug):
            self.skipTest("build the exam first: python3 build.py exam-ab1 --web")
        self.a, self.b = make_user("ana"), make_user("ben")

    def attempt(self, user):
        self.client.force_login(user)
        self.client.post(f"/exams/{self.slug}/start/")
        from course.models import ExamAttempt
        return ExamAttempt.objects.get(user=user, exam=self.slug, finished__isnull=True)

    def test_a_student_never_reaches_another_students_sitting(self):
        from course.models import ExamAttempt
        bens = self.attempt(self.b)
        self.client.force_login(self.a)
        base = f"/exams/{self.slug}/attempt/{bens.pk}/"
        self.assertEqual(self.client.get(base).status_code, 404)
        for action in ("state", "begin", "answer", "flag", "submit", "frq"):
            r = self.client.post(f"/api/exams/{self.slug}/{bens.pk}/{action}/", json.dumps({"item": "x", "value": "A"}),
                                 content_type="application/json")
            self.assertEqual(r.status_code, 404, action)
        self.client.post(base + "discard/")
        self.assertTrue(ExamAttempt.objects.filter(pk=bens.pk).exists())

    def test_garbage_bodies_get_4xx_not_500(self):
        att = self.attempt(self.a)
        bodies = ["[1]", "7", "nope", {"item": ["x"], "value": {"a": 1}}, {"part": None}, {"part": "1A", "checks": "yes"},
                  {"part": {"x": 1}, "checks": [1, 2]}, {"item": "z" * 5000, "on": "maybe"}]
        for action in ("state", "begin", "answer", "flag", "submit", "frq"):
            for body in bodies:
                r = self.client.post(f"/api/exams/{self.slug}/{att.pk}/{action}/",
                                     body if isinstance(body, str) else json.dumps(body), content_type="application/json")
                self.assertLess(r.status_code, 500, (action, body))

    def test_visitors_sign_in_first(self):
        self.client.logout()
        r = self.client.post(f"/exams/{self.slug}/start/")
        self.assertIn("/login/", r["Location"])
        self.assertEqual(self.client.get(f"/exams/{self.slug}/print/key/").status_code, 302)

    def test_slides_are_teacher_only(self):
        for who in (None, self.a):
            if who:
                self.client.force_login(who)
            for url in ("/teacher/slides/1.2/", "/teacher/slides/1.2/deck-blank.html"):
                self.assertEqual(self.client.get(url).status_code, 403, (who, url))


class Headers(TestCase):
    @override_settings(DESMOS_API_KEY="test-key")
    def test_csp_has_a_fresh_nonce_that_every_inline_script_carries(self):
        nonces = set()
        make_user("ana")
        self.client.login(username="ana", password=PW)
        for url in ("/course/", "/topic/2.1/", "/formulas/", "/exams/", "/exams/ab1/"):
            r = self.client.get(url)
            csp = r["Content-Security-Policy"]
            nonce = re.search(r"'nonce-([^']+)'", csp).group(1)
            nonces.add(nonce)
            self.assertIn("frame-ancestors 'none'", csp)
            script_src = csp.split("script-src")[1].split(";")[0]
            self.assertNotIn("'unsafe-inline'", script_src)
            # only pages that load the Desmos API (which evals) may eval
            self.assertEqual("'unsafe-eval'" in script_src, "www.desmos.com/api/" in r.content.decode(), url)
            for tag in re.findall(r"<script\b[^>]*>", r.content.decode()):
                if "src=" in tag or 'type="application/json"' in tag:
                    continue
                self.assertIn(f'nonce="{nonce}"', tag, url)
        self.assertEqual(len(nonces), 5)

    def test_slide_decks_are_made_csp_ready_when_served(self):
        from course.views import _csp_ready
        deck = ('<html lang="en"><body><script>\nwindow.deckTypeset = () => 1;\n</script>\n'
                '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.22/dist/contrib/auto-render.min.js" '
                'onload="window.deckTypeset()"></script>\n</body></html>')
        out = _csp_ready(deck, "N0NCE")
        self.assertNotIn("onload=", out)
        inline = [t for t in re.findall(r"<script\b[^>]*>", out) if "src=" not in t]
        self.assertEqual(len(inline), 2)
        self.assertTrue(all('nonce="N0NCE"' in t for t in inline))
        self.assertIn("DOMContentLoaded", out)

    def test_templates_have_no_inline_handlers_or_browser_dialogs(self):
        handler = re.compile(r"<[^>]+\son(click|load|error|submit|change|input)=", re.I)
        for p in list((WEB / "templates").rglob("*.html")):
            text = p.read_text()
            self.assertIsNone(handler.search(text), p)
            self.assertNotRegex(text, r"\b(alert|confirm|prompt)\(", p)
        for p in (WEB / "static" / "js").glob("*.js"):
            self.assertNotRegex(p.read_text(), r"(window\.|\s|^)(alert|confirm|prompt)\(", p)

    def test_safe_filter_only_on_author_content(self):
        """|safe is allowed on lesson content compiled from our own files and on fixed font strings, never on
        anything a user typed."""
        allowed = {"f.title|safe", "f.html|safe", "DESIGN_FONTS|safe"}
        for p in (WEB / "templates").rglob("*.html"):
            for m in re.findall(r"\{\{\s*([^}]*?\|safe)\s*\}\}", p.read_text()):
                self.assertIn(m.strip(), allowed, p)

    def test_cookies_and_links_are_scoped_to_the_mount(self):
        """Mounted at /calc/: links, static files and every cookie stay under the prefix, and the cookie names
        differ from the sibling apps' sessionid/csrftoken on the same host. Runs in a fresh process because the
        script prefix is read at startup."""
        code = (
            "import django; django.setup()\n"
            "from django.test.utils import setup_test_environment; setup_test_environment()\n"
            "from django.test import Client\n"
            "c = Client()\n"
            "r = c.get('/theme/paper/'); print(r['Location'], r.cookies['theme']['path'])\n"
            "r = c.get('/login/'); b = r.content.decode()\n"
            "print(r.cookies['calc_csrftoken']['path'], '/calc/static/css/app.css' in b, 'href=\"/calc/password-reset/\"' in b)\n")
        env = {**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings", "FORCE_SCRIPT_NAME": "/calc"}
        r = subprocess.run([sys.executable, "-c", code], cwd=WEB, env=env, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.split(), ["/calc/", "/calc/", "/calc/", "True", "True"])
        self.assertEqual((settings.SESSION_COOKIE_NAME, settings.CSRF_COOKIE_NAME), ("calc_session", "calc_csrftoken"))

    def test_legal_pages_are_marked_draft_until_reviewed(self):
        for url in ("/privacy/", "/terms/"):
            self.assertContains(self.client.get(url), "has not been reviewed yet")
            with override_settings(LEGAL_PAGES_REVIEWED=True):
                self.assertNotContains(self.client.get(url), "has not been reviewed yet")
        self.assertContains(self.client.get("/course/"), 'href="/privacy/"')

    def test_videos_are_not_collected(self):
        from django.contrib.staticfiles.utils import matches_patterns
        from django.apps import apps
        pats = apps.get_app_config("staticfiles").ignore_patterns
        self.assertTrue(matches_patterns("video/1_1.mp4", pats))
        self.assertTrue(matches_patterns("video", pats))
        self.assertFalse(matches_patterns("js/lesson.js", pats))


class ProductionSettings(TestCase):
    """Load config.production in a clean process with a production-like environment."""

    def run_py(self, code, **env):
        base = {k: v for k, v in os.environ.items() if not k.startswith(("DB_", "SECRET", "EMAIL", "DEFAULT_FROM"))}
        base.update({"DJANGO_SETTINGS_MODULE": "config.production", "CALC_ENV": "production",
                     "SECRET_KEY": "Zq8Rk2Lw5Tn9Vb4Xc7Mh3Jd6Pf1Gs0Ya" * 2, "DB_NAME": "calc", "EMAIL_HOST": "smtp.example.com",
                     "DEFAULT_FROM_EMAIL": "AP Calculus <noreply@example.com>", "ALLOWED_HOSTS": "adderoaks.com"})
        base.update(env)
        return subprocess.run([sys.executable, "-c", code], cwd=WEB, env=base, capture_output=True, text=True)

    def test_values(self):
        r = self.run_py("import django; django.setup(); from django.conf import settings as s; "
                        "print(s.DEBUG, s.FORCE_SCRIPT_NAME, s.SESSION_COOKIE_PATH, s.CSRF_TRUSTED_ORIGINS, "
                        "s.SESSION_COOKIE_SECURE, s.SECURE_HSTS_SECONDS, s.EMAIL_BACKEND.rsplit('.', 1)[1])")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), "False /calc /calc/ ['https://adderoaks.com'] True 31536000 EmailBackend")

    def test_bad_secret_keys_refuse_to_start(self):
        for key in ("", "short", "abc#" + "x" * 60, "x" * 40 + "'" + "y" * 20):
            r = self.run_py("import django; django.setup()", SECRET_KEY=key)
            self.assertNotEqual(r.returncode, 0, key)
            self.assertIn("SECRET_KEY", r.stderr)

    def test_generated_key_is_accepted(self):
        key = subprocess.run([sys.executable, str(WEB.parent / "scripts" / "gen_secret_key.py")],
                             capture_output=True, text=True).stdout.strip()
        self.assertRegex(key, r"^[A-Za-z0-9]{64}$")
        self.assertEqual(self.run_py("import django; django.setup()", SECRET_KEY=key).returncode, 0)

    def test_check_deploy_is_clean(self):
        r = self.run_py("import sys; from django.core.management import execute_from_command_line; "
                        "execute_from_command_line(['manage.py', 'check', '--deploy', '--fail-level', 'WARNING'])")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("no issues", r.stdout + r.stderr)
