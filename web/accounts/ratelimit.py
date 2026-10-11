"""A small cache-based rate limiter (fixed windows), so the app needs no extra dependency.

    @ratelimit("login", "ip", 60, 600)          # 60 tries per 10 minutes per client address

Limits are per key and window; counts live in the default cache, which production shares between gunicorn
workers (a database table). Classrooms share one public address behind the school's NAT, so the per-address
limits are set for thirty students at once; per-account limits are the tight ones.
"""
import functools
import hashlib
import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render

from .security import client_ip


def _key(group, ident, window):
    bucket = int(time.time() // window)
    h = hashlib.sha256(f"{group}|{ident}".encode()).hexdigest()[:32]
    return f"rl:{group}:{h}:{bucket}", window - int(time.time() % window) + 1


def hit(group, ident, limit, window):
    """Count one event; True when it is over the limit."""
    if not getattr(settings, "RATELIMIT_ENABLED", True):
        return False
    key, ttl = _key(group, ident, window)
    if cache.add(key, 1, ttl):
        n = 1
    else:
        try:
            n = cache.incr(key)
        except ValueError:          # expired between add and incr
            cache.set(key, 1, ttl)
            n = 1
    return n > limit


def is_limited(group, ident, limit, window):
    """Peek without counting."""
    if not getattr(settings, "RATELIMIT_ENABLED", True):
        return False
    key, _ = _key(group, ident, window)
    return (cache.get(key) or 0) >= limit


def ident_for(request, by):
    if by == "user" and request.user.is_authenticated:
        return f"u{request.user.pk}"
    return "ip" + client_ip(request)


def too_many(request, json=False):
    if json or "/api/" in request.path:
        return JsonResponse({"error": "too many requests, slow down a little"}, status=429)
    return render(request, "accounts/too_many.html", status=429)


def ratelimit(group, by, limit, window, methods=("POST",), json=False):
    """Decorator. `by` is "ip" or "user" (signed-in user, else address)."""
    def deco(view):
        @functools.wraps(view)
        def wrapped(request, *a, **kw):
            if request.method in methods and hit(group, ident_for(request, by), limit, window):
                return too_many(request, json)
            return view(request, *a, **kw)
        return wrapped
    return deco
