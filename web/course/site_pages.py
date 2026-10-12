"""The front-of-house pages: the landing page's numbers, About, and Contact (saved, then emailed through Resend)."""
import json
import logging
import urllib.error
import urllib.request

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.antibot import HumanCheckMixin
from accounts.ratelimit import ratelimit
from accounts.security import client_ip

from . import content, exams
from .models import ContactMessage

log = logging.getLogger(__name__)
HOUR = 3600
RESEND_URL = "https://api.resend.com/emails"
SENDER_NAME = "Mr Oaks Math"


# ------------------------------------------------------------------ landing page numbers
def course_facts():
    """Real counts from the built course, for the landing page. Cached for ten minutes: it opens every lesson file."""
    facts = cache.get("landing-facts")
    if facts:
        return facts
    have = content.available()
    course = module = practice = mcq = frq = videos = 0
    for u in content.syllabus():
        for t in u["topics"]:
            if t["n"] not in have:
                continue
            if u["module"]:
                module += 1
            else:
                course += 1
            pub = content.public(t["n"]) or {}
            practice += len(pub.get("practice", []))
            mcq += len(pub.get("mcq", []))
            frq += len(pub.get("frq", []))
            if (settings.VIDEO_DIR / f"{content.slug(t['n'])}.mp4").is_file():
                videos += 1
    facts = {"lessons": course, "module_lessons": module, "practice": practice, "mcq": mcq, "frq": frq,
             "practice_str": f"{practice:,}", "videos": videos, "unit_tests": len(content.unit_tests()), "exams": len(exams.available())}
    cache.set("landing-facts", facts, 600)
    return facts


# ------------------------------------------------------------------ about
def about(request):
    return render(request, "site/about.html")


# ------------------------------------------------------------------ contact
class ContactForm(HumanCheckMixin, forms.Form):
    name = forms.CharField(label="Your name", max_length=80)
    email = forms.EmailField(label="Your email", max_length=254, help_text="Used only to reply to you.")
    topic = forms.ChoiceField(label="What it's about", choices=ContactMessage.TOPICS)
    message = forms.CharField(label="Message", max_length=5000, widget=forms.Textarea(attrs={"rows": 7}))

    def clean_name(self):
        return " ".join(self.cleaned_data["name"].split())

    def clean_message(self):
        m = self.cleaned_data["message"].strip()
        if len(m) < 5:
            raise forms.ValidationError("Write a little more so I know how to help.")
        return m


def _sender():
    addr = settings.CONTACT_FROM.strip()
    return addr if "<" in addr else f"{SENDER_NAME} <{addr}>"


def resend_payload(msg):
    topic = msg.get_topic_display()
    text = (f"{msg.message}\n\n"
            f"From: {msg.name} <{msg.email}>\nTopic: {topic}\n"
            f"Account: {msg.user.username if msg.user else 'not signed in'}\nMessage #{msg.pk} in the admin.")
    return {"from": _sender(), "to": [settings.CONTACT_TO], "reply_to": msg.email,
            "subject": f"Mr Oaks Math contact: {topic}, from {msg.name}"[:180], "text": text}


def send_contact(msg):
    """Email one saved message to Adder through Resend. Records the outcome on the row; never raises."""
    if not settings.RESEND_API_KEY:
        log.info("contact message %s saved; RESEND_API_KEY is empty, so no email was sent", msg.pk)
        msg.error = "Sending is off (no RESEND_API_KEY)."
    elif not settings.CONTACT_TO or not settings.CONTACT_FROM:
        log.error("contact message %s saved but not sent: CONTACT_TO or CONTACT_FROM is empty", msg.pk)
        msg.error = "CONTACT_TO or CONTACT_FROM is not set."
    else:
        req = urllib.request.Request(RESEND_URL, data=json.dumps(resend_payload(msg)).encode(), method="POST", headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json",
            "User-Agent": "mroaksmath-contact/1"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                ok = 200 <= r.status < 300
                body = r.read(2000).decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            ok, body = False, f"HTTP {e.code}: {e.read(500).decode('utf-8', 'replace')}"
        except (urllib.error.URLError, OSError, ValueError) as e:
            ok, body = False, f"{type(e).__name__}: {e}"
        msg.sent = ok
        msg.error = "" if ok else body[:300]
        if not ok:
            log.error("contact message %s not sent through Resend: %s", msg.pk, body[:300])
    msg.save(update_fields=["sent", "error"])
    return msg.sent


@ratelimit("contact", "ip", 5, HOUR)
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            msg = ContactMessage.objects.create(name=d["name"], email=d["email"], topic=d["topic"], message=d["message"],
                                                user=request.user if request.user.is_authenticated else None,
                                                ip=client_ip(request))
            send_contact(msg)
            return redirect(reverse("contact") + "?sent=1")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial["email"] = request.user.email
            profile = getattr(request.user, "profile", None)
            if profile:
                initial["name"] = profile.display_name
        if request.GET.get("topic") in dict(ContactMessage.TOPICS):
            initial["topic"] = request.GET["topic"]
        form = ContactForm(initial=initial)
    return render(request, "site/contact.html", {"form": form, "sent": request.GET.get("sent") == "1"})
