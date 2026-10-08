"""Settings for the course site. One file; production differences come from the environment.

Local dev reads ../.env (DESMOS_API_KEY etc.). In production, systemd's EnvironmentFile
provides the same variables and CALC_ENV=production.
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
            os.environ.setdefault(k.strip(), v.strip())


_load_dotenv(REPO / ".env")

PROD = os.environ.get("CALC_ENV") == "production"
DEBUG = not PROD
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-not-secret")
if PROD and SECRET_KEY == "dev-only-not-secret":
    raise RuntimeError("SECRET_KEY must be set in production")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost" if PROD else "*").split(",")
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o]
FORCE_SCRIPT_NAME = os.environ.get("FORCE_SCRIPT_NAME") or None

DESMOS_API_KEY = os.environ.get("DESMOS_API_KEY", "")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "course",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
    }}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

AUTH_PASSWORD_VALIDATORS = [{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
                             "OPTIONS": {"min_length": 6}}]
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = False
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": ("whitenoise.storage.CompressedManifestStaticFilesStorage" if PROD
                                else "django.contrib.staticfiles.storage.StaticFilesStorage")},
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Teacher slide decks (tools/build_slides.py). Kept outside static/ so nginx never serves them to just anyone; Django
# checks the account first. With SLIDES_ACCEL set (e.g. "/protected-slides/"), Django answers with X-Accel-Redirect
# to that internal nginx location instead of streaming the file itself (docs/teacher-slides.md).
SLIDES_DIR = Path(os.environ.get("SLIDES_DIR") or REPO / "build" / "slides")
SLIDES_ACCEL = os.environ.get("SLIDES_ACCEL", "")

if PROD:
    SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
