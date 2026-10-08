"""Content-Security-Policy with a per-request nonce, and the client address behind nginx.

Inline <script> blocks carry nonce="{{ CSP_NONCE }}"; nothing else inline may run. Styles stay
'unsafe-inline' because KaTeX, MathLive and Desmos all write style attributes at runtime.
Third-party origins the pages need:
  cdn.jsdelivr.net   KaTeX (script, css, fonts) and MathLive (script, fonts, keypress sounds)
  fonts.googleapis.com / fonts.gstatic.com   web fonts for the designs
  www.desmos.com (and its subdomains)        the graphing calculator, with its images and fonts
"""
import secrets

from django.conf import settings

JSDELIVR = "https://cdn.jsdelivr.net"
DESMOS = "https://www.desmos.com https://*.desmos.com"


def policy(nonce):
    return "; ".join([
        "default-src 'self'",
        f"script-src 'self' 'nonce-{nonce}' {JSDELIVR} {DESMOS}",
        f"style-src 'self' 'unsafe-inline' https://fonts.googleapis.com {JSDELIVR} {DESMOS}",
        f"font-src 'self' data: https://fonts.gstatic.com {JSDELIVR} {DESMOS}",
        f"img-src 'self' data: blob: {DESMOS}",
        f"connect-src 'self' {DESMOS}",
        f"media-src 'self' {JSDELIVR}",
        "worker-src 'self' blob:",
        "frame-src 'none'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ])


class ContentSecurityPolicyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.csp_nonce = secrets.token_urlsafe(16)
        response = self.get_response(request)
        if getattr(settings, "CSP_ENABLED", True) and "Content-Security-Policy" not in response:
            name = "Content-Security-Policy-Report-Only" if settings.CSP_REPORT_ONLY else "Content-Security-Policy"
            response[name] = policy(request.csp_nonce)
        response.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()")
        return response


def client_ip(request):
    """The visitor's address. In production nginx sets X-Real-IP to $remote_addr (overwriting anything the
    client sent), and gunicorn only listens on 127.0.0.1, so the header can be trusted there."""
    ip = request.META.get(settings.CLIENT_IP_HEADER) or request.META.get("REMOTE_ADDR") or "unknown"
    return ip.split(",")[0].strip()[:64]
