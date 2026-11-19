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
- **The dataset dump**, `Drugcentral_2026-09-25.pgdump` (1.4 GB; ask the DrugCentral team), and about **15 GB of free disk** (8 GB image + ~5 GB data)
- **git**

## 2. Install the Python dependencies

```bash
cd /home/mpradhan/Research_Project/CFDE_IDG_DRS_v2
python -m venv venv
venv/bin/pip install -r requirements-dev.txt     # app + test dependencies
```

`requirements.txt` alone installs only what the API needs; `requirements-dev.txt` adds pytest and httpx.

## 3. Get a database

**Option A — restore a local copy (recommended).** One command creates a PostgreSQL 16
container with the RDKit cartridge (image `unmtransinfo/drugcen-2027-db`), loads the dump,
adds the API's indexes, creates the read-only user and writes `.env`:

```bash
scripts/restore_local_db.sh path/to/Drugcentral_2026-09-25.pgdump
```

It takes about 15 minutes, most of it loading the two largest tables. When it finishes you
have a container listening on `127.0.0.1:5435` with database `drugcentral`.

> On chiltepin this is already done: the container `drugcentral-2027` is running and holds the
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
DATABASE_URL=postgresql://drs_readonly:<password>@127.0.0.1:5435/drugcentral
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
curl http://127.0.0.1:8010/dbversion # {"version":56,"dtime":"2026-09-02T00:55:33.731000"}
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
venv/bin/pytest                 # 414 integration tests, about 40 seconds
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
docker exec -it drugcentral-2027 psql -U postgres -d drugcentral

# useful one-liners
docker exec drugcentral-2027 psql -U postgres -d drugcentral -c "select * from dbversion"
docker exec drugcentral-2027 psql -U postgres -d drugcentral -c "\d pk_az"
```

The API connects as `drs_readonly`, which can only read; `psql -U postgres` is the admin user.
`db/indexes.sql` holds the indexes the API's lookups need, and `db/api_readonly_role.sql`
creates that user. Both are safe to re-run.

## 10. Stopping and cleaning up

```bash
docker stop drugcentral-2027       # stop the database (data is kept)
docker start drugcentral-2027      # start it again
```

The data lives in the Docker volume `drugcentral-2027-data`, not in the container, so removing
the container keeps the data. Deleting that volume means restoring the dump again.

## 11. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `RuntimeError: DATABASE_URL is not set` | No `.env`, or you started uvicorn without `--env-file .env` |
| `/health` returns 503 | The database is down or unreachable: `docker ps`, then `docker start drugcentral-2027` |
| `503 Database busy, try again later` | All 15 pooled connections are in use; something is running many slow queries at once |
| `504 Database query timed out` | A query exceeded 30 seconds; narrow the request |
| `Address already in use` | Another process has that port; pick another (avoid 8000 and 8007 on chiltepin) |
| A lookup returns 404 that used to work | Identifiers now match exactly. A partial InChIKey or accession no longer matches; use the full value |
| Substring searches feel slow | `/faers/meddra_name/...` and similar scan whole tables (about 250 ms) since a substring can't use an index |
| `git status` shows the 1.4 GB dump | It isn't ignored. Stage files by name; never run `git add .` in this repo |

---

## What is left to do

Everything in the original migration plan is done except the items below, which is why the
plan file is no longer needed. As of 2026-11-19, v2 (version 2.0.0) is live at
https://api.drugcentral.org, where all 152 endpoints pass, and is tested (414 tests). A test
deployment also runs on chiltepin at https://chiltepin.health.unm.edu/drs/. Nothing has been
pushed to GitHub; the repository has no remote.

### Background worth keeping

- **Where the data comes from:** the dataset snapshot `Drugcentral_2026-09-25.pgdump`
  (dbversion 56 plus the Inxight integration and RDKit chemistry columns), built by Bivek
  Panthi on shishito and copied to chiltepin. The database he runs on
  `shishito.health.unm.edu` is not reachable from outside the UNM network, so the API never
  connects to it; it reads this restored copy instead.
- **Production:** the App Runner service `cfde-idg-drs-api` (us-east-2) runs the ECR image
  `cfde-idg-drs-api:v2.0.0` (us-east-1), at https://api.drugcentral.org and at the service's
  original address, https://uxn2ycvimg.us-east-2.awsapprunner.com. The image v1 ran is tagged
  `v1` in ECR for rollback. The database is v1's, `unmtid-dbs.net:5433`, upgraded to
  dbversion 56. The `drugcentral.org` DNS zone is in Route 53 in the same AWS account; keep
  its two `_…acm-validations.aws` records, which renew the HTTPS certificate.
- **Who to ask:** Bivek Panthi for the DrugCentral database and dumps; Dr. Jeremy Yang for
  what the API should expose (he approved `pk_az`); Dr. Cristian Bologa for `pk_az` itself.

### Open items

1. **Review v2 with your professor** and get approval before creating the GitHub repository.
2. **Point the DrugCentral website's API link at https://api.drugcentral.org/docs.** It still
   links to the old App Runner address, which works because that address serves the same
   service. Bivek maintains the site.
3. **Switch to a read-only login.** v2 runs with v1's login, `drugman`, which can write. The
   API's own sessions are read-only, but the real safeguard is a read-only login: ask Bivek to
   create one (`db/api_readonly_role.sql`) and to run `db/indexes.sql`, then change
   `DATABASE_URL`. Only after that should `drugman`'s password be changed; it is in v1's code
   and in this repository's history.
4. **Make the API easier for AI tools to use correctly** (from the DC27 AI-readiness email):
   return the release, the data cutoff and the CC BY-SA 4.0 license with every response
   (today only `/dbversion` and `/health` report the version); mark `pk_az` values as model
   predictions in the responses, not only in the documentation; and add endpoints for
   approvals, drug-drug interactions and labels, whose tables exist in dbversion 56 (Dr. Yang
   decides what the API exposes).
5. **Create the GitHub repository** under the department organization and push, after
   `drugman`'s password has been changed (item 3).
6. **Tell known v1 users about the change.** Identifiers now match exactly, so some partial
   lookups that worked in v1 return 404 in v2.
7. **Ask Dr. Bologa about the missing `pk_az` units** for `mh-clint` and `mppb`, whose sibling
   property types do have units.
8. **Rewrite `DEPLOYMENT.md`** for how v2 is actually deployed: push a new image tag to ECR,
   update the existing App Runner service to it, and the `api.drugcentral.org` custom domain.
   A later move to ECS Express Mode, which AWS recommends in place of App Runner, needs only a
   DNS change.

### Optional improvements

- **Cap `limit` and add rate limiting.** There is no maximum page size today, so one request
  can ask for an entire table. This matters most on a public URL, and the DRS development plan
  also mentions API keys.
- **Slim the Docker image.** It installs `gcc` and `postgresql-client`, which the app doesn't
  need (`psycopg2-binary` ships prebuilt). Removing them makes the 486 MB image smaller and
  the build much faster.
- **Index `structures.inchikey` upstream.** Neither DrugCentral release ships that index;
  `db/indexes.sql` adds it to our copies.
