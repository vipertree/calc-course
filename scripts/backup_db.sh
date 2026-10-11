#!/usr/bin/env bash
# Nightly Postgres dump of the course database, keeping BACKUP_DAYS days (default 14).
# Install (as deploy@):  crontab -e  then
#   17 3 * * * /home/deploy/calc-course/scripts/backup_db.sh >> /home/deploy/backups/calc/backup.log 2>&1
# Restore steps are in DEPLOYMENT.md. Keep a copy off the server too (see there).
set -euo pipefail
APP=/home/deploy/calc-course
DEST=${BACKUP_DIR:-/home/deploy/backups/calc}
set -a; . "$APP/.env"; set +a
DAYS=${BACKUP_DAYS:-14}
umask 077
mkdir -p "$DEST"
STAMP=$(date -u +%Y%m%d-%H%M%S)
OUT="$DEST/calc-$STAMP.dump"
PGPASSWORD="$DB_PASSWORD" pg_dump --format=custom --no-owner --no-privileges \
    -h "${DB_HOST:-127.0.0.1}" -p "${DB_PORT:-5432}" -U "$DB_USER" "$DB_NAME" > "$OUT.part"
mv "$OUT.part" "$OUT"
pg_restore --list "$OUT" > /dev/null          # fails loudly if the dump is unreadable
find "$DEST" -name 'calc-*.dump' -mtime +"$DAYS" -delete
echo "$(date -u +%FT%TZ) ok $OUT $(du -h "$OUT" | cut -f1)"
