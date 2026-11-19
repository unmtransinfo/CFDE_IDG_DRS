"""Concrete requests for every API route, built from real values in the database.

Shared by tests/test_every_endpoint.py and scripts/check_endpoints.py.
"""
import csv
import io
import json
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote

from fastapi.routing import APIRoute
from sqlalchemy import text

from app.main import app
from app.models import Base

MODELS = {mapper.class_.__tablename__: mapper.class_ for mapper in Base.registry.mappers}
# Columns holding pipe-separated lists; the API matches each entry.
PIPE_LISTS = {("act_table_full", "accession"), ("act_table_full", "swissprot")}
LIST_LIMIT = 5


@dataclass
class Case:
    route: str                   # route template, e.g. /structures/id/{id}
    path: str                    # request path with a real value (?skip&limit for list routes)
    missing_path: Optional[str]  # same route with a value that matches nothing (None for lists)
    kind: str                    # "json", "csv" or "tsv"
    pk_columns: tuple
    pk: Optional[tuple]          # primary key of a row the response must include (lookups only)


STATUS_ROUTES = ("/", "/health", "/dbversion")  # not table lookups; checked separately


def api_routes():
    return [r for r in app.routes if isinstance(r, APIRoute) and r.path not in STATUS_ROUTES]


def _sample(conn, table, column, pk_columns):
    """The least frequent usable value of a column (keeps responses small), plus the
    primary key of one row that has it. Skips values that cannot sit in a URL path."""
    value = f"split_part({column}, '|', 1)" if (table, column) in PIPE_LISTS else f"{column}::text"
    value_t = value.replace(column, f"t.{column}", 1)
    pk_t = ", ".join(f"t.{c}" for c in pk_columns)
    return conn.execute(text(
        f"with v as (select {value} as v, count(*) as n from {table} "
        f"  where {value} <> '' and {value} = btrim({value}) and {value} !~ '[/%\\\\?#]' "
        f"  group by 1 order by n, 1 limit 1) "
        f"select v.v, {pk_t} from {table} t join v on {value_t} = v.v order by {pk_t} limit 1")).one()


def build_cases(conn):
    cases, samples = [], {}
    for route in api_routes():
        segs = route.path.strip("/").split("/")
        table = segs[0]
        model = MODELS[table]
        pk_columns = tuple(c.name for c in model.__mapper__.primary_key)
        kind = segs[-1] if segs[-1] in ("csv", "tsv") else "json"
        if len(segs) == 1 or (len(segs) == 2 and kind != "json"):
            cases.append(Case(route.path, f"{route.path}?skip=0&limit={LIST_LIMIT}", None, kind, pk_columns, None))
            continue
        column, param = segs[1], segs[2]
        if (table, column) not in samples:
            samples[table, column] = _sample(conn, table, column, pk_columns)
        row = samples[table, column]
        bogus = "-1" if model.__table__.c[column].type.python_type is int else "zz-no-such-value-zz"
        cases.append(Case(route.path, route.path.replace(param, quote(row[0], safe="")),
                          route.path.replace(param, bogus), kind, pk_columns, tuple(row[1:])))
    return cases


def response_rows(kind, content):
    """Rows of a response body: a list of dicts for JSON and for CSV/TSV (header -> value)."""
    if kind == "json":
        return json.loads(content)
    return list(csv.DictReader(io.StringIO(content.decode()), delimiter="," if kind == "csv" else "\t"))


def contains_pk(rows, pk_columns, pk):
    want = tuple(str(v).strip() for v in pk)
    return any(tuple(str(row[c]).strip() for c in pk_columns) == want for row in rows)
