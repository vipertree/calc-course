"""Settings for the course site: development defaults. config/production.py builds on this module.

Local dev reads ../.env (DESMOS_API_KEY etc.). In production, systemd's EnvironmentFile provides the
variables, including CALC_ENV=production, which makes manage.py and wsgi.py pick config.production.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPO = BASE_DIR.parent


def _load_dotenv(path):
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_dotenv(REPO / ".env")


def env_list(name, default=""):
    return [x.strip() for x in os.environ.get(name, default).split(",") if x.strip()]


def env_bool(name, default=False):
    v = os.environ.get(name)
    return default if v is None else v.strip().lower() in ("1", "true", "yes", "on")


DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-only-not-secret"
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "*")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

# Mounted under a path prefix in production (adderoaks.com/calc/). Cookies are scoped to that path and
# given their own names so they never collide with the sibling Django apps on the same host.
FORCE_SCRIPT_NAME = (os.environ.get("FORCE_SCRIPT_NAME") or "").rstrip("/") or None
COOKIE_PATH = (FORCE_SCRIPT_NAME or "") + "/"
SESSION_COOKIE_NAME = "calc_session"
CSRF_COOKIE_NAME = "calc_csrftoken"
SESSION_COOKIE_PATH = CSRF_COOKIE_PATH = LANGUAGE_COOKIE_PATH = COOKIE_PATH
SESSION_COOKIE_SAMESITE = CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30          # a month; students sign in on shared school devices too

DESMOS_API_KEY = os.environ.get("DESMOS_API_KEY", "")
# Payments: Stripe is not connected yet (course/payments.py). Empty keys keep checkout off and the pages say so.
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "config.apps.CalcStaticFilesConfig",
    "accounts",
    "course",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "accounts.security.ContentSecurityPolicyMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "course.context.site",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"

if os.environ.get("DB_NAME"):
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", ""),
        "PORT": os.environ.get("DB_PORT", ""),
        "CONN_MAX_AGE": 60,
        "CONN_HEALTH_CHECKS": True,
    }}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

# Rate limits count in the cache. One process in dev, so local memory is enough; production shares
# counts between gunicorn workers through the database cache table (manage.py createcachetable).
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "calc"}}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTHENTICATION_BACKENDS = ["accounts.backends.UsernameOrEmailBackend"]
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"   # never in a readable cookie
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"
PASSWORD_RESET_TIMEOUT = 60 * 60 * 3            # reset links work for three hours
EMAIL_VERIFY_DAYS = 3                           # sign-up and email-change links
UNVERIFIED_ACCOUNT_DAYS = 14
BACKUP_DAYS = int(os.environ.get("BACKUP_DAYS", 14))   # scripts/backup_db.sh keeps this many daily dumps                    # purge_unverified removes self sign-ups never confirmed

# Email: printed to the console in development. Production sends over SMTP (see config/production.py).
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "AP Calculus <noreply@localhost>")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
ADMINS = [("Admin", a) for a in env_list("ADMIN_EMAILS")]

# Contact page (course/site_pages.py): every message is saved, then emailed to CONTACT_TO through Resend's HTTP API.
# An empty RESEND_API_KEY (development) skips the email and logs it; the message is still in the admin.
# CONTACT_FROM is a bare address on a domain verified in Resend (contact@adderoaks.com); the sender name is added.
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
CONTACT_TO = os.environ.get("CONTACT_TO", "")
CONTACT_FROM = os.environ.get("CONTACT_FROM", "")

# Bot checks on public forms: a hidden honeypot field plus a minimum time between page load and submit.
HUMAN_MIN_SECONDS = 3
HUMAN_MAX_SECONDS = 60 * 60 * 24
# Where the client address comes from. Behind nginx it is a header nginx sets (production.py).
CLIENT_IP_HEADER = "REMOTE_ADDR"
RATELIMIT_ENABLED = True
TEST_RUNNER = "config.test_runner.Runner"

# The legal pages are drafts until Adder (and ideally a lawyer) has read them. While False they say so.
LEGAL_PAGES_REVIEWED = env_bool("LEGAL_PAGES_REVIEWED", False)
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "")              # shown on the privacy page; Adder picks it

# Content-Security-Policy (accounts/security.py). Report-only lets a new third-party script be tried safely.
CSP_ENABLED = True
CSP_REPORT_ONLY = False

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = False
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
# Lesson videos are big and never collected: nginx serves them straight from this folder in production.
VIDEO_DIR = Path(os.environ.get("VIDEO_DIR") or BASE_DIR / "static" / "video")
# Printable PDFs compiled by ../build.py (packets, handouts, paper tests). Never public: views stamp and serve them.
PDF_DIR = Path(os.environ.get("PDF_DIR") or REPO / "build" / "pdf")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Teacher slide decks (tools/build_slides.py). Kept outside static/ so nginx never serves them to just anyone; Django
# checks the account first. With SLIDES_ACCEL set (e.g. "/protected-slides/"), Django answers with X-Accel-Redirect
# to that internal nginx location instead of streaming the file itself (docs/teacher-slides.md).
SLIDES_DIR = Path(os.environ.get("SLIDES_DIR") or REPO / "build" / "slides")
SLIDES_ACCEL = os.environ.get("SLIDES_ACCEL", "")
