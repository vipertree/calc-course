"""Who may do what. Every teacher-only view goes through teacher_required."""
import functools

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render


def profile_of(user):
    return getattr(user, "profile", None) if user.is_authenticated else None


def is_teacher(user):
    p = profile_of(user)
    return bool(p and p.is_teacher)


def forbidden(request, message="This page is for teachers."):
    return render(request, "accounts/forbidden.html", {"message": message}, status=403)


def teacher_required(view):
    @functools.wraps(view)
    def wrapped(request, *a, **kw):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if not is_teacher(request.user):
            return forbidden(request)
        return view(request, *a, **kw)
    return wrapped
