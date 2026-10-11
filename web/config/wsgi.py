import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "config.production" if os.environ.get("CALC_ENV") == "production" else "config.settings")
application = get_wsgi_application()
