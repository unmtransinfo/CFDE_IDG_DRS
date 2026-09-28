# DrugCentral DRS API v2 on chiltepin

A test deployment for the DrugCentral team, running on `chiltepin.health.unm.edu`. It is
separate from the eventual AWS deployment, and from the live v1 API.

| | |
|---|---|
| API | https://chiltepin.health.unm.edu/drs/ |
| Interactive docs | https://chiltepin.health.unm.edu/drs/docs |
| Health check | https://chiltepin.health.unm.edu/drs/health |
| Data | DrugCentral dbversion 56 (2026-09-02) + Inxight integration, on PostgreSQL 16 with the RDKit cartridge |

The API is read-only and unauthenticated: it only runs `SELECT` queries, as a database user
that cannot write.

## Using it

```bash
curl https://chiltepin.health.unm.edu/drs/health
curl "https://chiltepin.health.unm.edu/drs/structures?limit=5"
curl "https://chiltepin.health.unm.edu/drs/structures/inchikey/LIOLIMKSCNQPLV-UHFFFAOYSA-N"
curl "https://chiltepin.health.unm.edu/drs/pk_az/struct_id/4"
curl "https://chiltepin.health.unm.edu/drs/structures/csv?limit=100" -o structures.csv
```

See the repository README for the full endpoint list, matching rules and error codes.

## How it runs

Two containers, defined in `compose.yml`:

| Container | What it is |
|---|---|
| `drugcentral-drs-api` | The API image, published on `127.0.0.1:8007` only |
| `drugcentral-2027` | PostgreSQL 16 + RDKit (`unmtransinfo/drugcen-2027-db` image) with the DrugCentral data, on `127.0.0.1:5435` for local use |

The API reaches the database over a private Docker network, so nothing but Apache can reach
the API and nothing outside this machine can reach the database. Apache serves the API at
`/drs/` (see `apache-drugcentral-drs-api.conf`). Both containers restart automatically,
including after a reboot.

## Operating it

```bash
cd /home/mpradhan/Research_Project/CFDE_IDG_DRS_v2

# status and logs
docker compose -f deploy/chiltepin/compose.yml ps
docker compose -f deploy/chiltepin/compose.yml logs -f api

# start / stop
docker compose -f deploy/chiltepin/compose.yml up -d
docker compose -f deploy/chiltepin/compose.yml stop

# deploy a new version of the API (rebuild the image, restart only the API)
docker compose -f deploy/chiltepin/compose.yml build api
docker compose -f deploy/chiltepin/compose.yml up -d api

# check the deployment: every endpoint, several times each
venv/bin/python scripts/check_endpoints.py --base http://127.0.0.1:8007 --repeat 3
```

Settings live in `deploy/chiltepin/.env` (not in git; see `.env.example`).

## First-time setup

1. Restore the data, if the `drugcentral-2027-data` volume does not exist yet:
   `scripts/restore_local_db.sh path/to/Drugcentral_2026-09-25.pgdump` (about 15 minutes).
2. Create `deploy/chiltepin/.env` from `.env.example`, using the read-only user's password.
3. `docker compose -f deploy/chiltepin/compose.yml up -d`
4. Install the Apache configuration (needs root):
   ```bash
   sudo cp deploy/chiltepin/apache-drugcentral-drs-api.conf /etc/apache2/sites-available/drugcentral-drs-api.conf
   # add to the :80 and :443 virtual hosts in /etc/apache2/sites-enabled/000-default.conf
   # and 000-default-le-ssl.conf:
   #   Include /etc/apache2/sites-available/drugcentral-drs-api.conf
   sudo apache2ctl configtest && sudo systemctl reload apache2
   ```

## Updating the data to a new DrugCentral release

Restore the new dump into a fresh volume and point the deployment at it, rather than
overwriting the running one:

```bash
CONTAINER=drugcentral-next PORT=5436 VOLUME=drugcentral-next-data \
  scripts/restore_local_db.sh path/to/Drugcentral_<new-date>.pgdump
```
Then change the volume name in `compose.yml`, run `docker compose ... up -d`, and check
`/drs/health` reports the new `dbversion`. Keeping the old volume makes rolling back a
one-line change.
