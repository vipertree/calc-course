"""Production settings. Selected by CALC_ENV=production (manage.py, wsgi.py) or --settings=config.production.

Everything secret or host-specific comes from the environment (the server's .env, loaded by systemd's
EnvironmentFile and by `set -a; . ./.env; set +a` before manage.py). See DEPLOYMENT.md.
"""
import os
import re

from django.core.exceptions import ImproperlyConfigured

from .settings import *  # noqa: F401,F403
from .settings import env_bool, env_list


def _required(name):
    v = os.environ.get(name, "").strip()
    if not v:
        raise ImproperlyConfigured(f"{name} must be set in production (see DEPLOYMENT.md)")
    return v


DEBUG = False

# Alphanumeric only: a '#' or quote in a sourced .env silently truncates the value (it once emptied a
# sibling app's key and every POST 500'd). Generate with scripts/gen_secret_key.py on the server.
SECRET_KEY = _required("SECRET_KEY")
if not re.fullmatch(r"[A-Za-z0-9]{50,}", SECRET_KEY):
    raise ImproperlyConfigured("SECRET_KEY must be at least 50 letters and digits, nothing else "
                               "(python3 scripts/gen_secret_key.py)")

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS") or ["adderoaks.com"]
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS") or [f"https://{h}" for h in ALLOWED_HOSTS]

# Path-prefix mount: nginx proxies https://adderoaks.com/calc/ to gunicorn with the prefix stripped.
FORCE_SCRIPT_NAME = (os.environ.get("FORCE_SCRIPT_NAME", "/calc") or "").rstrip("/") or None
COOKIE_PATH = (FORCE_SCRIPT_NAME or "") + "/"
SESSION_COOKIE_PATH = CSRF_COOKIE_PATH = LANGUAGE_COOKIE_PATH = COOKIE_PATH
# Spelled out with the prefix: Django adds the script prefix to a relative STATIC_URL lazily and caches the first
# answer, which whitenoise asks for at startup, before any request has set the prefix (pages linked /static/...).
STATIC_URL = COOKIE_PATH + "static/"

if not os.environ.get("DB_NAME"):
    raise ImproperlyConfigured("DB_NAME (and DB_USER, DB_PASSWORD) must be set: production runs on Postgres")

CACHES = {"default": {"BACKEND": "django.core.cache.backends.db.DatabaseCache", "LOCATION": "calc_cache"}}

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# nginx terminates TLS and passes the scheme and the client address.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CLIENT_IP_HEADER = "HTTP_X_REAL_IP"
SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
# The adderoaks.com apps already send a one-year HSTS with subdomains and preload (mathfacts); match it.
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 31536000))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", True)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", True)

CSP_REPORT_ONLY = env_bool("CSP_REPORT_ONLY", False)

# Email over SMTP. Without EMAIL_HOST nothing can be sent, so sign-up verification and password reset
# would silently fail: refuse to start instead.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = _required("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", EMAIL_PORT == 587)
EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", EMAIL_PORT == 465)
EMAIL_TIMEOUT = 15
DEFAULT_FROM_EMAIL = _required("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"plain": {"format": "{levelname} {asctime} {name} {message}", "style": "{"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "plain"},
        "mail_admins": {"class": "django.utils.log.AdminEmailHandler", "level": "ERROR"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.request": {"handlers": ["console", "mail_admins"], "level": "ERROR", "propagate": False},
        "django.security": {"handlers": ["console", "mail_admins"], "level": "WARNING", "propagate": False},
    },
}
