#!/bin/bash
# Restore an official DrugCentral dump into a local Postgres container for development,
# add the API's indexes (db/indexes.sql) and create the read-only API role
# (db/api_readonly_role.sql).
#
# usage: scripts/restore_local_db.sh path/to/Drugcentral_YYYY-MM-DD.pgdump
# env:   CONTAINER (default drugcentral-2027), PORT (default 5435),
#        VOLUME (default <CONTAINER>-data), WRITE_ENV=1 to overwrite an existing .env,
#        IMAGE (default unmtransinfo/drugcen-2027-db:pg16-rdkit2026.03.6)
#
# The dump is pg_dump custom format and its chemistry columns need the RDKit
# cartridge, so it must be restored into the dataset image (PostgreSQL 16 +
# RDKit), not a stock postgres image.
#
# The container listens on 127.0.0.1 only. Admin access needs no password:
#   docker exec -it <CONTAINER> psql -U postgres -d drugcentral
set -euo pipefail

DUMP=${1:?usage: $0 path/to/Drugcentral_YYYY-MM-DD.pgdump}
CONTAINER=${CONTAINER:-drugcentral-2027}
PORT=${PORT:-5435}
VOLUME=${VOLUME:-$CONTAINER-data}
IMAGE=${IMAGE:-unmtransinfo/drugcen-2027-db:pg16-rdkit2026.03.6}
DB=drugcentral
REPO=$(cd "$(dirname "$0")/.." && pwd)

log() { echo "[$(date +%H:%M:%S)] $*"; }
secret() { python3 -c 'import secrets; print(secrets.token_hex(24))'; }

[ -f "$DUMP" ] || { echo "dump not found: $DUMP" >&2; exit 1; }
if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "container $CONTAINER already exists; remove it first or set CONTAINER=..." >&2
    exit 1
fi

log "starting $CONTAINER ($IMAGE) on 127.0.0.1:$PORT"
# /dev/null over the image's baked-in init script disables it: we drive the
# restore ourselves, so the seed dump baked into the image is ignored.
docker run -d --name "$CONTAINER" --restart unless-stopped \
    -e POSTGRES_PASSWORD="$(secret)" -e POSTGRES_DB="$DB" \
    -p "127.0.0.1:$PORT:5432" -v "$VOLUME:/var/lib/postgresql/data" \
    -v "$(readlink -f "$DUMP"):/docker-entrypoint/seed.pgdump:ro" \
    -v /dev/null:/docker-entrypoint-initdb.d/wait-for-db.sh:ro \
    "$IMAGE" -c maintenance_work_mem=1GB -c max_wal_size=4GB >/dev/null
timeout 180 bash -c "until docker logs $CONTAINER 2>&1 | grep -q 'PostgreSQL init process complete'; do sleep 1; done"
timeout 60 bash -c "until docker exec $CONTAINER pg_isready -q -U postgres -d $DB; do sleep 1; done"

psql_admin() { docker exec -i "$CONTAINER" psql -U postgres -d "$DB" -v ON_ERROR_STOP=1 -q "$@"; }

log "creating the rdkit extension (the dump's chemistry columns need it)"
psql_admin -c "CREATE EXTENSION IF NOT EXISTS rdkit;"

log "restoring $DUMP (pg_dump custom format, about 15 minutes)"
docker exec "$CONTAINER" pg_restore -U postgres -d "$DB" --no-owner --no-privileges --exit-on-error /docker-entrypoint/seed.pgdump

log "adding API indexes"
psql_admin < "$REPO/db/indexes.sql"

log "creating read-only role drs_readonly"
API_PASSWORD=$(secret)
# The password goes in on stdin, so it never appears in a process list.
{ printf "\\\\set api_password '%s'\n" "$API_PASSWORD"; cat "$REPO/db/api_readonly_role.sql"; } | psql_admin

URL="postgresql://drs_readonly:$API_PASSWORD@127.0.0.1:$PORT/$DB"
if [ -e "$REPO/.env" ] && [ -z "${WRITE_ENV:-}" ]; then
    log ".env exists and was left unchanged; to use this database set in it:"
    echo "  DATABASE_URL=$URL"
else
    (umask 177; printf 'DATABASE_URL=%s\n' "$URL" > "$REPO/.env")
    log "wrote DATABASE_URL to $REPO/.env"
fi
log "done: $(docker exec "$CONTAINER" psql -U postgres -d "$DB" -tAc "select 'dbversion ' || version || ' (' || dtime || ')' from dbversion")"
