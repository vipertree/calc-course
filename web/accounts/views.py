import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core import signing
from django.core.mail import mail_admins, send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import forms as F
from .models import Classroom, Enrollment, Profile
from .ratelimit import hit, ident_for, is_limited, ratelimit, too_many

VERIFY_SALT = "calc.verify-email"
HOUR, DAY = 3600, 86400


# ------------------------------------------------------------------ email confirmation
def verify_token(user, email):
    """A link that sets `email` on `user` and marks it confirmed. It names the address the account had
    when it was sent, so once the email changes again every older link stops working."""
    return signing.dumps({"u": user.pk, "e": email, "cur": user.email}, salt=VERIFY_SALT, compress=True)


def send_verification(request, user, email):
    link = request.build_absolute_uri(reverse("verify_email", args=[verify_token(user, email)]))
    ctx = {"name": user.profile.display_name, "link": link, "days": settings.EMAIL_VERIFY_DAYS}
    send_mail("Confirm your email for AP Calculus", render_to_string("accounts/email/verify.txt", ctx),
              None, [email])


def verify_email(request, token):
    try:
        d = signing.loads(token, salt=VERIFY_SALT, max_age=settings.EMAIL_VERIFY_DAYS * DAY)
    except signing.SignatureExpired:
        return render(request, "accounts/verify.html", {"ok": False, "expired": True}, status=400)
    except signing.BadSignature:
        return render(request, "accounts/verify.html", {"ok": False}, status=400)
    user = User.objects.filter(pk=d["u"]).select_related("profile").first()
    if user is None or user.email != d["cur"]:
        return render(request, "accounts/verify.html", {"ok": False}, status=400)
    if F.email_in_use(d["e"], exclude=user):
        return render(request, "accounts/verify.html", {"ok": False, "taken": True}, status=400)
    user.email = d["e"]
    user.save(update_fields=["email"])
    user.profile.email_verified = True
    user.profile.save(update_fields=["email_verified"])
    return render(request, "accounts/verify.html", {"ok": True, "email": d["e"]})


@login_required
@require_POST
@ratelimit("resend", "user", 3, HOUR)
def resend_verification(request):
    p = request.user.profile
    if request.user.email and not p.email_verified:
        send_verification(request, request.user, request.user.email)
        messages.success(request, f"We sent a new link to {request.user.email}.")
    return redirect("account")


# ------------------------------------------------------------------ sign in, sign up
class LoginView(auth_views.LoginView):
    """Django's login, limited per address (generous: a class shares one) and per account name (tight)."""
    template_name = "accounts/login.html"

    def post(self, request, *a, **kw):
        if hit("login-ip", ident_for(request, "ip"), 60, 10 * 60):
            return too_many(request)
        name = (request.POST.get("username") or "").strip().lower()[:254]
        if name and is_limited("login-user", name, 10, 15 * 60):
            return too_many(request)
        return super().post(request, *a, **kw)

    def form_invalid(self, form):
        name = (self.request.POST.get("username") or "").strip().lower()[:254]
        if name:
            hit("login-user", name, 10, 15 * 60)
        return super().form_invalid(form)


def _new_user(form, role=Profile.STUDENT, email="", **profile):
    u = User.objects.create_user(form.cleaned_data["username"], email=email, password=form.cleaned_data["password"])
    Profile.objects.create(user=u, role=role, display_name=form.cleaned_data["display_name"], **profile)
    return u


@ratelimit("join", "ip", 60, HOUR)
def join(request):
    if request.user.is_authenticated:
        form = F.JoinExistingForm(request.POST or None, initial={"code": request.GET.get("code", "")})
        if request.method == "POST" and form.is_valid():
            if getattr(request.user, "profile", None) and request.user.profile.is_teacher:
                form.add_error("code", "Teacher accounts can't join a class. Use a student account.")
            else:
                Enrollment.objects.get_or_create(classroom=form.classroom, student=request.user)
                return redirect("home")
        return render(request, "accounts/join.html", {"form": form, "existing": True})
    form = F.JoinForm(request.POST or None, initial={"code": request.GET.get("code", "")})
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            u = _new_user(form)
            Enrollment.objects.create(classroom=form.classroom, student=u)
        login(request, u, backend=settings.AUTHENTICATION_BACKENDS[0])
        return redirect("home")
    return render(request, "accounts/join.html", {"form": form})


@ratelimit("signup", "ip", 10, HOUR)
def signup(request):
    if request.user.is_authenticated:
        return redirect("account")
    form = F.SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            u = _new_user(form, email=form.cleaned_data["email"])
        send_verification(request, u, u.email)
        login(request, u, backend=settings.AUTHENTICATION_BACKENDS[0])
        messages.success(request, f"Welcome! We sent a link to {u.email}. Open it to confirm your email.")
        return redirect("home")
    return render(request, "accounts/signup.html", {"form": form, "teacher": False})


@ratelimit("signup", "ip", 10, HOUR)
def teacher_signup(request):
    """Asks for a teacher account. Teacher accounts see answer keys, so a person approves each one
    (admin: Profiles, action "Approve teacher request", or manage.py approve_teacher)."""
    if request.user.is_authenticated:
        return redirect("account")
    form = F.TeacherSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            u = _new_user(form, email=form.cleaned_data["email"], teacher_requested=timezone.now(),
                          school=form.cleaned_data["school"].strip())
        send_verification(request, u, u.email)
        mail_admins("Teacher account request",
                    f"{u.profile.display_name} ({u.username}, {u.email}) asked for a teacher account.\n"
                    f"School: {u.profile.school or '(not given)'}\nApprove it in the admin under Profiles once "
                    f"their email is confirmed.", fail_silently=True)
        login(request, u, backend=settings.AUTHENTICATION_BACKENDS[0])
        return redirect("account")
    return render(request, "accounts/signup.html", {"form": form, "teacher": True})


# ------------------------------------------------------------------ password reset (Django's flow, our pages)
class PasswordResetView(auth_views.PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/email/password_reset.txt"
    subject_template_name = "accounts/email/password_reset_subject.txt"
    form_class = F.PasswordResetForm
    success_url = reverse_lazy("password_reset_done")

    def post(self, request, *a, **kw):
        if hit("reset-ip", ident_for(request, "ip"), 10, HOUR):
            return too_many(request)
        return super().post(request, *a, **kw)

    def form_valid(self, form):
        # at most three emails an hour to any one address, however many people ask
        if hit("reset-email", form.cleaned_data["email"].strip().lower(), 3, HOUR):
            return redirect(self.success_url)
        return super().form_valid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


# ------------------------------------------------------------------ account settings
def _account_page(request, **forms):
    p = request.user.profile
    ctx = {
        "p": p,
        "name_form": forms.get("name_form") or F.NameForm(initial={"display_name": p.display_name}),
        "email_form": forms.get("email_form") or F.EmailChangeForm(request.user),
        "password_form": forms.get("password_form") or PasswordChangeForm(request.user),
        "delete_form": forms.get("delete_form") or F.DeleteAccountForm(request.user),
        "classes": Classroom.objects.filter(enrollments__student=request.user).select_related("teacher__profile"),
        "teaching": Classroom.objects.filter(teacher=request.user) if p.is_teacher else [],
        "open": forms.get("open", ""),
    }
    return render(request, "accounts/account.html", ctx, status=400 if forms.get("open") else 200)


@never_cache
@login_required
def account(request):
    if getattr(request.user, "profile", None) is None:
        Profile.objects.create(user=request.user, display_name=request.user.get_username(),
                               role=Profile.TEACHER if request.user.is_superuser else Profile.STUDENT)
    return _account_page(request)


@login_required
@require_POST
def account_name(request):
    form = F.NameForm(request.POST)
    if not form.is_valid():
        return _account_page(request, name_form=form, open="name")
    request.user.profile.display_name = form.cleaned_data["display_name"]
    request.user.profile.save(update_fields=["display_name"])
    messages.success(request, "Name saved.")
    return redirect("account")


@login_required
@require_POST
@ratelimit("email-change", "user", 5, HOUR)
def account_email(request):
    form = F.EmailChangeForm(request.user, request.POST)
    if not form.is_valid():
        return _account_page(request, email_form=form, open="email")
    send_verification(request, request.user, form.cleaned_data["email"])
    messages.success(request, f"We sent a link to {form.cleaned_data['email']}. "
                              "Your email changes when you open it.")
    return redirect("account")


@login_required
@require_POST
@ratelimit("password-change", "user", 10, HOUR)
def account_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if not form.is_valid():
        return _account_page(request, password_form=form, open="password")
    form.save()
    update_session_auth_hash(request, form.user)
    messages.success(request, "Password changed.")
    return redirect("account")


@login_required
@require_POST
def leave_class(request, pk):
    Enrollment.objects.filter(classroom_id=pk, student=request.user).delete()
    messages.success(request, "You left the class. Your own work stays in your account.")
    return redirect("account")


@login_required
@require_POST
@ratelimit("delete", "user", 10, HOUR)
def account_delete(request):
    form = F.DeleteAccountForm(request.user, request.POST)
    if not form.is_valid():
        return _account_page(request, delete_form=form, open="delete")
    user = request.user
    logout(request)
    user.delete()           # cascades: profile, classes taught, enrollments, answers, drafts, scores, packets
    return render(request, "accounts/deleted.html")


@never_cache
@login_required
def account_export(request):
    """Everything stored about the signed-in person, as JSON."""
    from course.models import Draft, FRQScore, IssuedPacket, QuizAttempt, Response, StepDone
    u = request.user
    p = getattr(u, "profile", None)
    t = lambda d: d.isoformat() if d else None        # noqa: E731
    data = {
        "exported": t(timezone.now()),
        "account": {"username": u.username, "email": u.email, "joined": t(u.date_joined), "last_login": t(u.last_login),
                    "display_name": p and p.display_name, "role": p and p.role, "email_confirmed": p and p.email_verified,
                    "school": p and p.school, "full_access": p and p.full_access},
        "classes_joined": [{"class": e.classroom.name, "teacher": getattr(e.classroom.teacher, "profile", None)
                            and e.classroom.teacher.profile.display_name, "joined": t(e.joined)}
                           for e in u.enrollments.select_related("classroom__teacher__profile")],
        "classes_teaching": [{"class": c.name, "code": c.code, "course": c.course, "open": c.open,
                              "created": t(c.created), "students": c.enrollments.count()}
                             for c in u.classrooms.all()],
        "lesson_steps_done": [{"topic": s.topic, "step": s.step, "at": t(s.at)} for s in StepDone.objects.filter(user=u)],
        "answers_checked": [{"topic": r.topic, "item": r.item, "area": r.area, "given": r.given, "correct": r.correct,
                             "at": t(r.at)} for r in Response.objects.filter(user=u).order_by("at")],
        "saved_drafts": [{"topic": d.topic, "item": d.item, "value": d.value, "answer_shown": d.revealed,
                          "updated": t(d.updated)} for d in Draft.objects.filter(user=u)],
        "quiz_and_test_attempts": [{"topic": a.topic, "score": a.score, "total": a.total, "answers": a.detail,
                                    "form": a.form, "at": t(a.at)} for a in QuizAttempt.objects.filter(user=u)],
        "frq_self_scores": [{"topic": s.topic, "part": s.part, "earned": s.earned, "possible": s.possible,
                             "at": t(s.at)} for s in FRQScore.objects.filter(user=u)],
        "printed_packets": [{"topic": k.topic, "code": k.code, "created": t(k.created)}
                            for k in IssuedPacket.objects.filter(user=u)],
    }
    resp = HttpResponse(json.dumps(data, indent=2), content_type="application/json")
    resp["Content-Disposition"] = f'attachment; filename="ap-calculus-{u.username}.json"'
    return resp


# ------------------------------------------------------------------ static pages
def privacy(request):
    return render(request, "accounts/privacy.html")


def terms(request):
    return render(request, "accounts/terms.html")
