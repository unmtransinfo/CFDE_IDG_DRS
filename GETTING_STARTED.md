# Getting started: running and using the API locally

This is the DrugCentral DRS API v2. It is a read-only REST API over a PostgreSQL copy of
DrugCentral (**dbversion 56, 2026-09-02**), serving JSON, CSV and TSV.

Everything below runs on your own machine. For the shared test deployment, see
[deploy/chiltepin/README.md](deploy/chiltepin/README.md); for the endpoint reference, see
[README.md](README.md).

---

## 1. Prerequisites

- **Python 3.11 or newer**
- **Docker**, to run the database locally (not needed if you point at a database someone else hosts)
- **The DrugCentral dump**, `drugcentral.dump.09022026.sql.gz` (1.4 GB), and about **6 GB of free disk**
- **git**

## 2. Install the Python dependencies

```bash
cd /home/mpradhan/Research_Project/CFDE_IDG_DRS_v2
python -m venv venv
venv/bin/pip install -r requirements-dev.txt     # app + test dependencies
```

`requirements.txt` alone installs only what the API needs; `requirements-dev.txt` adds pytest and httpx.

## 3. Get a database

**Option A — restore a local copy (recommended).** One command creates a PostgreSQL 14
container, loads the dump, adds the API's indexes, creates the read-only user and writes
`.env`:

```bash
scripts/restore_local_db.sh path/to/drugcentral.dump.09022026.sql.gz
```

It takes about 15 minutes, most of it loading the two largest tables. When it finishes you
have a container listening on `127.0.0.1:5434` with database `drugcentral`.

> On chiltepin this is already done: the container `drugcentral-v56` is running and holds the
> data, so you can skip to step 4.

**Option B — use an existing DrugCentral database.** Copy the template and fill in the
connection string:

```bash
cp .env.example .env
# DATABASE_URL=postgresql://user:password@host:5432/drugcentral
```

The database must be dbversion 56 or newer; `pk_az` does not exist in older releases.

## 4. Check your settings

`.env` holds one setting, and it is git-ignored:

```
DATABASE_URL=postgresql://drs_readonly:<password>@127.0.0.1:5434/drugcentral
```

The API refuses to start if `DATABASE_URL` is missing, rather than failing later.

## 5. Start the server

```bash
venv/bin/uvicorn app.main:app --env-file .env --host 127.0.0.1 --port 8010
```

You should see `Application startup complete` and `Uvicorn running on http://127.0.0.1:8010`.
Add `--reload` while editing code to restart on save.

> **On chiltepin, don't use port 8000.** Apache proxies `/` on the public site to
> `127.0.0.1:8000`, so a server there would be reachable from the internet. Port 8007 is also
> taken, by the team deployment.

## 6. Verify it works

```bash
curl http://127.0.0.1:8010/          # {"status":"ok"} - the process is up
curl http://127.0.0.1:8010/health    # {"status":"ok","database":"ok","dbversion":56}
```

If `/` works but `/health` returns 503, the API is running but cannot reach the database:
check that the database container is running (`docker ps`) and that `DATABASE_URL` is right.

Interactive documentation, with every endpoint and a "Try it out" button:
**http://127.0.0.1:8010/docs**

## 7. Using the API

Each of the 23 tables has the same three shapes of endpoint. Examples use `$API=http://127.0.0.1:8010`.

**List rows** (ordered by primary key, so pages are stable):

```bash
curl "$API/structures?limit=5"
curl "$API/structures?skip=100&limit=50"
```

**Look up by a column** — `/{table}/{column}/{value}`:

```bash
curl "$API/structures/id/5392"                                  # capmatinib
curl "$API/structures/inchikey/LIOLIMKSCNQPLV-UHFFFAOYSA-N"     # exact, case-insensitive
curl "$API/structures/name/capmat"                              # names are substring searches
curl "$API/act_table_full/struct_id/5392"                       # its bioactivities
curl "$API/act_table_full/accession/P02919"                     # matches multi-component targets too
curl "$API/atc/code/N02B"                                       # an ATC group (codes match by prefix)
curl "$API/faers/struct_id/5392"                                # adverse events
```

**Export CSV or TSV** — add `/csv` or `/tsv`:

```bash
curl "$API/structures/csv?limit=100" -o structures.csv
curl "$API/faers/struct_id/5392/csv" -o capmatinib_faers.csv
curl "$API/pk_az/type/herg/tsv" -o herg_predictions.tsv
```

**Predicted properties (`pk_az`, new in v2)** — AstraZeneca model predictions, not measurements:

```bash
curl "$API/pk_az/struct_id/4"          # all 25 predicted properties for one drug
curl "$API/pk_az/type/kinase-safety-class"
```

Which columns match exactly and which are substring searches is listed under
[Matching rules](README.md#matching-rules) in the README. In short: identifiers are exact and
case-insensitive, ATC codes match by prefix, and names and free text are substring searches.

**What the status codes mean:**

| Status | Meaning |
|---|---|
| 404 | Nothing matched the lookup |
| 422 | A parameter has the wrong type, e.g. text where a number is expected |
| 503 | The database is unreachable, or all its connections are busy |
| 504 | The query took longer than 30 seconds |

## 8. Run the tests

With `DATABASE_URL` pointing at a dbversion 56 database:

```bash
venv/bin/pytest                 # 383 integration tests, about 40 seconds
venv/bin/pytest tests/test_lookups.py -v     # one file, verbose
```

The tests run the API in-process, so you don't need a server running. They check health and
error handling, stable pagination, exact lookups against SQL, `pk_az`, CSV/TSV exports, and
every route with real values from the database.

To exercise a **running** server instead, calling every endpoint several times:

```bash
venv/bin/python scripts/check_endpoints.py --base http://127.0.0.1:8010 --repeat 5
```

It prints one line per endpoint (status, repeatability, row counts, timings) and exits
non-zero if anything fails.

## 9. Looking at the database directly

```bash
docker exec -it drugcentral-v56 psql -U postgres -d drugcentral

# useful one-liners
docker exec drugcentral-v56 psql -U postgres -d drugcentral -c "select * from dbversion"
docker exec drugcentral-v56 psql -U postgres -d drugcentral -c "\d pk_az"
```

The API connects as `drs_readonly`, which can only read; `psql -U postgres` is the admin user.
`db/indexes.sql` holds the indexes the API's lookups need, and `db/api_readonly_role.sql`
creates that user. Both are safe to re-run.

## 10. Stopping and cleaning up

```bash
docker stop drugcentral-v56        # stop the database (data is kept)
docker start drugcentral-v56       # start it again
```

The data lives in the Docker volume `drugcentral-v56-data`, not in the container, so removing
the container keeps the data. Deleting that volume means restoring the dump again.

## 11. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `RuntimeError: DATABASE_URL is not set` | No `.env`, or you started uvicorn without `--env-file .env` |
| `/health` returns 503 | The database is down or unreachable: `docker ps`, then `docker start drugcentral-v56` |
| `503 Database busy, try again later` | All 15 pooled connections are in use; something is running many slow queries at once |
| `504 Database query timed out` | A query exceeded 30 seconds; narrow the request |
| `Address already in use` | Another process has that port; pick another (avoid 8000 and 8007 on chiltepin) |
| A lookup returns 404 that used to work | Identifiers now match exactly. A partial InChIKey or accession no longer matches; use the full value |
| Substring searches feel slow | `/faers/meddra_name/...` and similar scan whole tables (about 250 ms) since a substring can't use an index |
| `git status` shows the 1.4 GB dump | It isn't ignored. Stage files by name; never run `git add .` in this repo |

---

## What is left to do

Everything in the original migration plan is done except the items below, which is why the
plan file is no longer needed. As of 2026-09-15, v2 is code-complete, tested (383 tests, all
151 endpoints verified repeatedly) and deployed on chiltepin for the team. Nothing has been
pushed to GitHub; the repository has no remote.

### Background worth keeping

- **Where the data comes from:** the official DrugCentral release dump,
  `drugcentral.dump.09022026.sql.gz` (dbversion 56). Bivek Panthi confirmed we may use a copy.
  The updated DrugCentral database he runs on `shishito.health.unm.edu` is not reachable from
  outside the UNM network, so the API never connects to it; it reads a restored copy instead.
- **v1 is unaffected:** it still serves the legacy database (dbversion 54) at
  https://uxn2ycvimg.us-east-2.awsapprunner.com from `unmtid-dbs.net:5433`.
- **Who to ask:** Bivek Panthi for the DrugCentral database and dumps; Dr. Jeremy Yang for
  what the API should expose (he approved `pk_az`); Dr. Cristian Bologa for `pk_az` itself.

### Open items

1. **Review v2 with your professor** and get approval before creating the GitHub repository.
2. **Decide who hosts the database for the AWS deployment.** If a publicly reachable v56
   database is provided (as `unmtid-dbs.net` does for v1), the API just points at it. If not,
   restore the dump into RDS. This question is with Bivek and Dr. Yang.
3. **Deploy to AWS.** App Runner is discontinued, so the target is ECS Fargate: push the image
   to ECR in the cluster's region, supply `DATABASE_URL` from Secrets Manager or SSM, send logs
   to CloudWatch, and point the load balancer's health check at `/` while an alarm watches
   `/health` (see the note in [DEPLOYMENT.md](DEPLOYMENT.md)). `DEPLOYMENT.md` still describes
   App Runner and needs rewriting for ECS.
4. **Add the public URL** to `README.md` and `DEPLOYMENT.md` once deployed.
5. **Create the GitHub repository** under the department organization and push.
6. **Decide what happens to v1:** run both in parallel, or retire v1 once v2 is validated, and
   tell known users about the new endpoint.
7. **Ask Dr. Bologa about the missing `pk_az` units** for `mh-clint` and `mppb`, whose sibling
   property types do have units.

### Optional improvements

- **Cap `limit` and add rate limiting.** There is no maximum page size today, so one request
  can ask for an entire table. This matters most on a public URL, and the DRS development plan
  also mentions API keys.
- **Slim the Docker image.** It installs `gcc` and `postgresql-client`, which the app doesn't
  need (`psycopg2-binary` ships prebuilt). Removing them makes the 486 MB image smaller and
  the build much faster.
- **Index `structures.inchikey` upstream.** Neither DrugCentral release ships that index;
  `db/indexes.sql` adds it to our copies.
