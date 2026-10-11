#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # CALC_ENV=production (set in the server's .env) selects the production settings, so a manage.py run
    # after `set -a; . ./.env; set +a` talks to Postgres and builds the hashed static manifest.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "config.production" if os.environ.get("CALC_ENV") == "production" else "config.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
