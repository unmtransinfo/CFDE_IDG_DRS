#!/usr/bin/env python3
"""Call every API endpoint several times against a running server and report the results.

usage: venv/bin/python scripts/check_endpoints.py [--base http://127.0.0.1:8000] [--repeat 5]

Sample values come from the database in DATABASE_URL (or .env), which should be the database
the server uses. For each endpoint it checks that every call returns HTTP 200, that the
response includes the row the sample value came from (or a full page for list routes), that
all calls returned the same data, and that an unknown value returns 404.
"""
import argparse
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(REPO / ".env")

from app.database import engine  # noqa: E402
from tests.samples import LIST_LIMIT, build_cases, contains_pk, response_rows  # noqa: E402

# Routes that are not table lookups, each with a check of its JSON body.
STATUS_CHECKS = (
    ("/", lambda body: body == {"status": "ok"}),
    ("/health", lambda body: body.get("database") == "ok" and body.get("dbversion", 0) >= 56),
    ("/dbversion", lambda body: body.get("version", 0) >= 56 and bool(body.get("dtime"))),
)


def fetch(url):
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            return r.status, r.read(), time.perf_counter() - start
    except urllib.error.HTTPError as e:
        return e.code, e.read(), time.perf_counter() - start


def run_case(base, path, repeat, check, missing_path=None, kind="json"):
    """Call path `repeat` times; return (ok, summary fields)."""
    calls = [fetch(base + path) for _ in range(repeat)]
    statuses = [s for s, _, _ in calls]
    ok_status = all(s == 200 for s in statuses)
    rows = [response_rows(kind, body) for _, body, _ in calls] if ok_status else []
    ok_same = ok_status and all(r == rows[0] for r in rows)
    ok_content = ok_status and check(rows[0])
    ok_404 = missing_path is None or fetch(base + missing_path)[0] == 404
    ms = sorted(t * 1000 for _, _, t in calls)
    n_rows = len(rows[0]) if ok_status and isinstance(rows[0], list) else "-"
    return ok_status and ok_same and ok_content and ok_404, {
        "200s": f"{statuses.count(200)}/{repeat}", "same": "yes" if ok_same else "NO",
        "content": "yes" if ok_content else "NO", "404": "-" if missing_path is None else ("yes" if ok_404 else "NO"),
        "rows": n_rows, "ms": f"{ms[0]:.0f}/{statistics.median(ms):.0f}/{ms[-1]:.0f}",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="http://127.0.0.1:8000", help="API base URL")
    parser.add_argument("--repeat", type=int, default=5, help="calls per endpoint")
    args = parser.parse_args()

    with engine.connect() as conn:
        cases = build_cases(conn)
    print(f"{len(cases) + len(STATUS_CHECKS)} endpoints x {args.repeat} calls each, against {args.base}\n")
    print(f"{'result':6} {'endpoint':44} {'fmt':4} {'rows':>6} {'200s':>5} {'same':>4} {'data':>4} {'404':>3}  ms min/med/max")

    failures = 0

    def report(ok, route, kind, s):
        nonlocal failures
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL':6} {route:44} {kind:4} {s['rows']!s:>6} {s['200s']:>5} {s['same']:>4} "
              f"{s['content']:>4} {s['404']:>3}  {s['ms']}")

    for path, check in STATUS_CHECKS:
        ok, s = run_case(args.base, path, args.repeat, check)
        report(ok, path, "json", s)
    for case in cases:
        if case.pk is None:
            def check(rows):
                return len(rows) == LIST_LIMIT
        else:
            def check(rows, case=case):
                return contains_pk(rows, case.pk_columns, case.pk)
        ok, s = run_case(args.base, case.path, args.repeat, check, case.missing_path, case.kind)
        report(ok, case.route, case.kind, s)

    total = len(cases) + len(STATUS_CHECKS)
    print(f"\n{total - failures}/{total} endpoints passed ({args.repeat} calls each)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
