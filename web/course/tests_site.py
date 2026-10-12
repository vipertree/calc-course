"""The landing, About and Contact pages. Contact saves every message, then emails it through Resend (mocked here)."""
import io
import json
import urllib.error
from unittest import mock

from django.contrib import admin
from django.core.cache import cache
from django.test import TestCase, override_settings

from accounts.antibot import stamp

from .models import ContactMessage

RESEND = dict(RESEND_API_KEY="re_test_123", CONTACT_TO="adder@example.com", CONTACT_FROM="contact@example.com")


class FakeResponse(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class Pages(TestCase):
    def test_pages_load(self):
        for url in ("/", "/about/", "/contact/"):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200, url)
            html = r.content.decode()
            self.assertNotIn("—", html, url)          # no em dashes, Adder's rule
            self.assertNotIn("&mdash;", html, url)
            self.assertIn('href="/about/"', html, url)       # footer links
            self.assertIn('href="/contact/"', html, url)

    def test_landing_links_into_the_site(self):
        html = self.client.get("/").content.decode()
        for href in ("/course/", "/formulas/", "/exams/", "/students/", "/teachers/", "/membership/", "/trig/", "/videos/"):
            self.assertIn(f'href="{href}"', html)
        self.assertIn("Mr Oaks Math", html)
        self.assertIn("autoplay muted loop playsinline", html)

    def test_about_has_adders_words_and_reach_out_link(self):
        html = self.client.get("/about/").content.decode()
        self.assertIn("Adder Oaks!</h1>", html)
        self.assertIn("A note about AI", html)
        self.assertIn('<a href="/contact/">reach out</a>', html)
        self.assertIn("img/adder-oaks.webp", html)


class Contact(TestCase):
    def setUp(self):
        cache.clear()

    def form(self, **kw):
        d = {"name": "Kai Moreno", "email": "kai@example.com", "topic": "school",
             "message": "Our district would like to use the course next year.", "website": "", "started": stamp(10)}
        d.update(kw)
        return d

    def test_saves_and_thanks_without_a_key(self):
        with mock.patch("course.site_pages.urllib.request.urlopen") as urlopen:
            r = self.client.post("/contact/", self.form())
        self.assertRedirects(r, "/contact/?sent=1")
        urlopen.assert_not_called()
        m = ContactMessage.objects.get()
        self.assertEqual((m.name, m.email, m.topic), ("Kai Moreno", "kai@example.com", "school"))
        self.assertFalse(m.sent)
        self.assertIn("RESEND_API_KEY", m.error)
        page = self.client.get(r["Location"]).content.decode()
        self.assertIn("Thanks for writing", page)
        self.assertNotIn("<form", page.split("<main")[1].split("</main>")[0])

    def test_honeypot_is_refused(self):
        r = self.client.post("/contact/", self.form(website="http://spam.example"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Something went wrong with that form")
        self.assertFalse(ContactMessage.objects.exists())

    def test_too_fast_is_refused(self):
        r = self.client.post("/contact/", self.form(started=stamp(0)))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())

    def test_missing_fields(self):
        r = self.client.post("/contact/", self.form(email="not-an-email", message=""))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(ContactMessage.objects.exists())

    @override_settings(RATELIMIT_ENABLED=True)
    def test_rate_limited(self):
        frozen = mock.patch("accounts.ratelimit.time.time", return_value=1_800_000_010.0)   # one fixed window
        frozen.start()
        self.addCleanup(frozen.stop)
        codes = [self.client.post("/contact/", self.form(started=stamp(10))).status_code for _ in range(6)]
        self.assertEqual(codes, [302] * 5 + [429])
        self.assertEqual(ContactMessage.objects.count(), 5)
        cache.clear()

    @override_settings(**RESEND)
    def test_sends_through_resend(self):
        with mock.patch("course.site_pages.urllib.request.urlopen", return_value=FakeResponse(b'{"id":"abc"}')) as urlopen:
            r = self.client.post("/contact/", self.form())
        self.assertRedirects(r, "/contact/?sent=1")
        req = urlopen.call_args.args[0]
        self.assertEqual(req.full_url, "https://api.resend.com/emails")
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(req.get_header("Authorization"), "Bearer re_test_123")
        self.assertEqual(req.get_header("Content-type"), "application/json")
        body = json.loads(req.data)
        self.assertEqual(body["from"], "Mr Oaks Math <contact@example.com>")
        self.assertEqual(body["to"], ["adder@example.com"])
        self.assertEqual(body["reply_to"], "kai@example.com")
        self.assertIn("School or district", body["subject"])
        self.assertIn("Kai Moreno", body["subject"])
        self.assertIn("Our district would like", body["text"])
        m = ContactMessage.objects.get()
        self.assertTrue(m.sent)
        self.assertEqual(m.error, "")

    @override_settings(**RESEND)
    def test_resend_failure_still_saves_and_thanks(self):
        err = urllib.error.HTTPError("https://api.resend.com/emails", 403, "Forbidden", {}, io.BytesIO(b'{"message":"domain not verified"}'))
        with mock.patch("course.site_pages.urllib.request.urlopen", side_effect=err):
            r = self.client.post("/contact/", self.form())
        self.assertRedirects(r, "/contact/?sent=1")
        m = ContactMessage.objects.get()
        self.assertFalse(m.sent)
        self.assertIn("403", m.error)

    def test_in_admin(self):
        self.assertIn(ContactMessage, admin.site._registry)
