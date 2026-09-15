"""Every route, called with a real value from the database: the response must include the row
the value came from (or a full page for list routes), and an unknown value must give 404."""
import pytest

from app.database import engine
from tests.samples import LIST_LIMIT, build_cases, contains_pk, response_rows

with engine.connect() as conn:
    CASES = build_cases(conn)


@pytest.mark.parametrize("case", CASES, ids=lambda c: c.route)
def test_endpoint_returns_expected_rows(client, case):
    r = client.get(case.path)
    assert r.status_code == 200
    rows = response_rows(case.kind, r.content)
    if case.pk is None:
        assert len(rows) == LIST_LIMIT
    else:
        assert contains_pk(rows, case.pk_columns, case.pk), f"expected the row with {case.pk_columns}={case.pk}"


@pytest.mark.parametrize("case", [c for c in CASES if c.missing_path], ids=lambda c: c.route)
def test_endpoint_returns_404_for_unknown_value(client, case):
    r = client.get(case.missing_path)
    assert r.status_code == 404
    assert r.json()["detail"].endswith("not found")
