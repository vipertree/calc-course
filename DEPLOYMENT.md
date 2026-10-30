# Deploying the AP Calculus course

**Live as a PREVIEW since 2026-10-30:** `https://adderoaks.com/calccoursepreview/`, the same layout as below
but with `FORCE_SCRIPT_NAME=/calccoursepreview`, and every location behind HTTP basic auth
(`deploy/nginx-calcpreview.conf`, password file `/etc/nginx/.htpasswd-calcpreview`, user `oaks`) with
`X-Robots-Tag: noindex`. It is for Adder's first students; the real launch moves to its own server. Email is
not configured (`EMAIL_HOST=localhost`, nothing listening): class-code students never need it, but self sign-up,
teacher requests and password-reset emails will fail. `FRQ_ARCHIVE` is off. Smoke test: every path must 401
without the password (`curl -s -o /dev/null -w "%{http_code}" https://adderoaks.com/calccoursepreview/video/1_1.mp4`).

**Planned (not yet deployed):** `https://adderoaks.com/calc/`, a path-prefix mount on the adderoaks vhost,
gunicorn on `127.0.0.1:8018`, Postgres database `calc`. Same shape as outrangeous / imitation / frogracer /
mathfacts. Port 8018 follows the workspace convention (local dev port = prod port) and is free in prod
(taken: 8000, 8003, 8005, 8006, 8008, 8011, 8082).

| Thing | Location |
|---|---|
| Code | `/home/deploy/calc-course` (clone of `vipertree/calc-course`, branch `main`) |
| Django project | `/home/deploy/calc-course/web` (run `manage.py` from here) |
| Secrets | `/home/deploy/calc-course/.env`, mode 600 (template: `.env.example`) |
| Virtualenv | `/home/deploy/calc-course/venv` |
| Static files | `web/staticfiles/` (world-readable; nginx serves `/calc/static/`) |
| Videos | `web/static/video/` (world-readable; nginx serves `/calc/video/`), **not in git**, rsynced from the dev machine |
| Printable PDFs | `build/pdf/` (**not** world-readable; Django stamps and serves them), **not in git**, rsynced |
| Lesson JSON | `web/course/content/*.json`, **not in git**, built by `build.py --web` (or rsynced) |
| Service | `calc.service` (`deploy/calc.service`), 3 gunicorn workers |
| Nginx | the blocks in `deploy/nginx-calc.conf`, inside the adderoaks.com 443 server block |
| Backups | `/home/deploy/backups/calc/`, nightly `scripts/backup_db.sh` |
| Logs | `sudo journalctl -u calc -f` |

## First deploy

As `deploy@` on the server:

```bash
cd /home/deploy
git clone https://github.com/vipertree/calc-course.git
cd calc-course
python3 -m venv venv
./venv/bin/pip install -r web/requirements.txt

# Postgres (as root/postgres): a role and a database
sudo -u postgres psql -c "CREATE ROLE calc LOGIN PASSWORD '<paste generated password>'"
sudo -u postgres createdb -O calc calc

# Secrets: generate ON THE SERVER, letters and digits only
python3 scripts/gen_secret_key.py      # SECRET_KEY
python3 scripts/gen_secret_key.py      # DB_PASSWORD (use the same one in CREATE ROLE above)
cp .env.example .env && chmod 600 .env && nano .env
```

Then, from the dev machine, ship what git doesn't carry (generated, large):

```bash
# lesson JSON + figures (or run `python3 build.py <topics> --web --no-pdf` on the server instead)
rsync -a web/course/content/ deploy@91.98.21.156:calc-course/web/course/content/
rsync -a web/static/figures/ deploy@91.98.21.156:calc-course/web/static/figures/
# PDFs (packets, handouts, paper tests) and the stamp font
rsync -a build/pdf/ deploy@91.98.21.156:calc-course/build/pdf/
# videos (about 1 GB now, about 2.7 GB when all lessons are rendered)
rsync -a --info=progress2 web/static/video/ deploy@91.98.21.156:calc-course/web/static/video/
```

Back on the server:

```bash
cd /home/deploy/calc-course/web
set -a; . ../.env; set +a                 # load-bearing: see "Things that bite"
../venv/bin/python manage.py check --deploy
../venv/bin/python manage.py migrate
../venv/bin/python manage.py createcachetable  # rate-limit counters live in the database
../venv/bin/python manage.py collectstatic --noinput
../venv/bin/python manage.py createsuperuser   # Adder's admin account
../venv/bin/python manage.py create_teacher adder "Adder Oaks" '<password>' --class "Period 3"   # optional

# nginx can reach static files and videos, and nothing else
chmod o+x /home/deploy/calc-course /home/deploy/calc-course/web /home/deploy/calc-course/web/static
chmod -R go+rX /home/deploy/calc-course/web/staticfiles /home/deploy/calc-course/web/static/video
chmod -R go-rwx /home/deploy/calc-course/build /home/deploy/calc-course/.env

sudo cp ../deploy/calc.service /etc/systemd/system/calc.service
sudo systemctl daemon-reload && sudo systemctl enable --now calc
curl -s -o /dev/null -w "%{http_code}\n" -H "Host: adderoaks.com" -H "X-Forwarded-Proto: https" http://127.0.0.1:8018/login/   # 200

# nginx: back up OUTSIDE sites-enabled, paste deploy/nginx-calc.conf into the 443 server block
sudo cp /etc/nginx/sites-enabled/adderoaks.com /etc/nginx/backups/adderoaks.com.$(date +%F)
sudo nano /etc/nginx/sites-enabled/adderoaks.com
sudo nginx -t && sudo systemctl reload nginx

# backups
mkdir -p /home/deploy/backups/calc && chmod 700 /home/deploy/backups
crontab -e     # 17 3 * * * /home/deploy/calc-course/scripts/backup_db.sh >> /home/deploy/backups/calc/backup.log 2>&1
# weekly cleanup of self sign-ups that never confirmed their email
#               30 3 * * 0 cd /home/deploy/calc-course/web && set -a && . ../.env && set +a && ../venv/bin/python manage.py purge_unverified
```

Smoke test from anywhere:

```bash
curl -sI https://adderoaks.com/calc/ | grep -iE "^HTTP|strict-transport|content-security"
curl -s -o /dev/null -w "%{http_code}\n" https://adderoaks.com/calc/static/css/app.css                 # 200 (nginx alias)
curl -s -o /dev/null -w "%{http_code}\n" -H "Range: bytes=0-99" https://adderoaks.com/calc/video/1_1.mp4   # 206
```

Then sign up as a test teacher at `/calc/signup/teacher/`, confirm the email (proves SMTP works), approve it
in `/calc/admin/` (Profiles, action "Approve teacher request") or with `manage.py approve_teacher <username>`,
make a class and join it from a private window with the code.

## Routine updates

```bash
cd /home/deploy/calc-course && git pull
cd web && set -a; . ../.env; set +a
../venv/bin/pip install -r requirements.txt
../venv/bin/python manage.py migrate
../venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart calc
```

Plus the rsyncs above for whatever was rebuilt (lesson JSON, PDFs, new videos). New videos need no restart.

## Accounts, in one paragraph

Students join with a teacher's class code and are **never asked for an email**; a teacher resets a forgotten
password from the dashboard (Manage students), and the new password is shown to the teacher once. Students may
add an email later in Account settings. People studying on their own sign up with an email (confirmed by link,
13 or older, checkbox). Teachers ask for an account at `/signup/teacher/`; it stays a student account until
Adder approves it, because teacher accounts see every answer key. Admins (ADMIN_EMAILS) get an email for each
request. Password reset by email only goes to confirmed addresses.

## Security settings (config/production.py)

- `CALC_ENV=production` in `.env` makes `manage.py` and `wsgi.py` load `config.production`.
- Refuses to start without: an alphanumeric `SECRET_KEY` of 50+ characters, `DB_NAME`, `EMAIL_HOST`, `DEFAULT_FROM_EMAIL`.
- HTTPS only: secure cookies, HSTS one year with subdomains and preload (same as mathfacts already sends for
  adderoaks.com), `SECURE_PROXY_SSL_HEADER` for nginx, SSL redirect.
- Cookies are named `calc_session` / `calc_csrftoken` and scoped to `/calc/`, so they never collide with the
  sibling Django apps on the same host.
- Content-Security-Policy with a per-request nonce (`accounts/security.py`). Allowed origins: jsDelivr (KaTeX,
  MathLive), Google Fonts, Desmos. Pages that load the Desmos API also allow `eval` (Desmos needs it). To try a
  new third-party script without breaking pages, set `CSP_REPORT_ONLY=true` for a while.
- Rate limits (`accounts/ratelimit.py`, counts in the database cache): sign-in 60 per 10 min per address and
  10 failures per 15 min per username; join-by-code 60/hour per address (a whole class shares the school's
  address); sign-up 10/hour per address; password reset 10/hour per address and 3/hour per email; answer checks
  300/min per student. nginx's `X-Real-IP` is what identifies an address.
- Bot checks on every public form: a hidden honeypot field and a signed "form shown at" time (at least 3 seconds,
  at most a day). No CAPTCHA.

## Backups and restore

`scripts/backup_db.sh` writes a custom-format `pg_dump` every night to `/home/deploy/backups/calc/`, checks it is
readable, and deletes dumps older than `BACKUP_DAYS` (14). The privacy page tells users deleted data leaves the
backups within that many days, so keep the two in step. **These dumps sit on the same server**; copy them off
too (for example a nightly `rsync` or `rclone` to a Hetzner Storage Box or the dev machine), or a lost server
loses both.

Restore into the live database:

```bash
sudo systemctl stop calc
sudo -u postgres dropdb calc && sudo -u postgres createdb -O calc calc
cd /home/deploy/calc-course/web && set -a; . ../.env; set +a
PGPASSWORD="$DB_PASSWORD" pg_restore --no-owner --role=calc -h 127.0.0.1 -U calc -d calc \
    /home/deploy/backups/calc/calc-YYYYMMDD-HHMMSS.dump
../venv/bin/python manage.py migrate         # only needed if the code is newer than the dump
sudo systemctl start calc
```

To test a dump without touching production, restore it into a scratch database (`createdb -O calc calc_restore_test`)
and point a one-off `DB_NAME=calc_restore_test manage.py shell` at it. Videos, PDFs and lesson JSON are rebuilt
from the repo and the dev machine, so they are not in the database backup.

## Videos: size and bandwidth

Measured 2026-10-08 in `web/static/video`: 103 MP4s averaging **10.3 MB** (largest 25 MB), about 1 GB in all.
Each lesson has a light and a dark version.

| | Estimate |
|---|---|
| Storage, ~130 lessons x 2 looks | 260 x 10.3 MB = **about 2.7 GB** |
| One lesson watched once | about 10 MB (a student watches one look) |
| A class of 30, 4 lessons a week | 30 x 16 x 10 MB = **about 5 GB/month** |
| 500 active students at that pace | **about 80 GB/month** |
| 5,000 active students | **about 800 GB/month** |

The current renders are 480p and silent; final renders with narration (and any higher resolution) will be
larger, so re-measure then (`du -sh web/static/video`). Hetzner Cloud servers include 20 TB/month of
traffic in EU locations (less in US ones), so traffic is not the limit; disk is. Check free space with `df -h`
before the first rsync. Videos are served by nginx with Range support (seeking works), `sendfile`, and a one-day
cache. If traffic ever matters, a CDN or object storage in front of `/calc/video/` is the next step.

## Teacher slide decks

Decks are built by `tools/build_slides.py` into `build/slides/` (not in git, rsync it like the PDFs) and served
to teachers only. See `docs/teacher-slides.md` for the optional `SLIDES_ACCEL` setting and its `internal`
nginx location, which lets nginx stream the files after Django has checked the account. Decks get the site's
CSP nonce added when served, so decks built before the policy work unchanged.

## AP FRQ Archive (/calc/frq/)

The released College Board free-response questions, rebuilt from Adder's old archive at `adderoaks.com/calcfrq/`.
Not in git: everything lives in `build/frq/` (set `FRQ_DIR` to move it). Rebuild on the dev machine, then rsync:

```bash
python3 tools/fetch_frq_archive.py                         # mirror the PDFs into build/frq/raw/ (polite, skips unchanged files)
~/opt/mamba/envs/calc/bin/python tools/build_frq_archive.py  # split question / scoring guidelines, render pages, write manifest.json
rsync -a --delete build/frq/manifest.json build/frq/files deploy@91.98.21.156:calc-course/build/frq/
```

`build/frq/files/<id>/` holds the page images (`q1.webp`, `s1.webp`, ...) and the original PDF. That folder is
public, so nginx serves it directly (`location ^~ /calc/frq/file/` in `deploy/nginx-calc.conf`), with
`image/webp` and `application/pdf` types and a week's cache. nginx has to reach it without opening `build/pdf/`:

```bash
chmod o+x /home/deploy/calc-course/build /home/deploy/calc-course/build/frq
chmod -R go+rX /home/deploy/calc-course/build/frq/files
chmod go-rwx /home/deploy/calc-course/build/frq/manifest.json   # gunicorn reads it; nobody else needs to
```

`build/pdf/` keeps its own `go-rwx`, so `o+x` on `build/` exposes nothing else. The manifest is read by
Django (`course/frq.py`) and picked up without a restart when it changes. With no manifest the archive pages
say it's empty instead of failing. Size: 171 questions, about 90 MB of images and PDFs in `files/` (the raw mirror is another 100 MB and stays on the dev machine).

## Things that bite

- **Source `.env` before any `manage.py` command.** Without `CALC_ENV=production` you get development settings:
  SQLite instead of Postgres, and `collectstatic` writes unhashed files the production manifest can't serve, so
  every page 500s. Recover with `collectstatic --clear --noinput` after sourcing `.env`.
- **Comments in `.env` go on their own line.** systemd keeps a `# ...` after a value as part of it.
- **Generate secrets on the server, alphanumeric only.** A `#` in a sourced value truncates it; production
  settings refuse a SECRET_KEY with anything but letters and digits.
- **nginx needs to traverse the project directory** (`chmod o+x`) to reach `staticfiles/` and the videos, and the
  `^~` prefixes are load-bearing: without them the vhost's static-extension regex serves `.mp4`/`.css` from `/var/www`.
- **Keep nginx backups out of `sites-enabled/`.** Backups go in `/etc/nginx/backups/`.
- **`collectstatic` skips `static/video/`** on purpose (`config/apps.py`); videos are served from that folder directly.
- **The Desmos key in the dev `.env` is a trial key** (the browser console says so). Production needs a key
  from Desmos.
- Tests run under development settings: `cd web && python manage.py test` (no `.env` needed). With
  `PDF_DIR`/`VIDEO_DIR` pointing at built files, the PDF and video tests run too.
