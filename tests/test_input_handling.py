"""Regression tests for the input-handling defects found in the independent review:
literal % and _ in substring searches, values that were decoded twice, out-of-range
pagination, and NUL characters. Values come from the database, not hardcoded rows."""
from urllib.parse import quote

import pytest

from app.main import get_db, read_product_by_product_name, read_structures_by_smiles

FIRST_PRODUCT_WITH_PERCENT = (
    "select product_name from product where strpos(product_name, '%') > 0 order by id limit 1")
FIRST_GENE_WITH_BACKSLASH = (
    "select gene from target_component where strpos(gene, chr(92)) > 0 order by id limit 1")


def path(*parts):
    return "/" + "/".join(quote(str(p), safe="") for p in parts)


@pytest.fixture
def db():
    """A database session, for calling handlers directly."""
    sessions = get_db()
    session = next(sessions)
    try:
        yield session
    finally:
        sessions.close()


# I1: FastAPI already decodes a path parameter; decoding it again changed the value.
# These two call the handler directly: Starlette's test client decodes percent-escapes
# differently from uvicorn, so an in-process request cannot carry "%" reliably. Over HTTP
# these are GET /product/product_name/Vitamin%20c%2020%25Face%20Cream and
# GET /structures/smiles/%2510.
def test_literal_percent_in_a_value_is_found(db, sql):
    name = sql(FIRST_PRODUCT_WITH_PERCENT)
    if name is None:
        pytest.skip("no product name contains % in this release")
    rows = read_product_by_product_name(name, db)
    assert any(row.product_name == name for row in rows)


def test_percent_sequence_is_treated_as_text(db, sql):
    # "%10" as text: decoded a second time it would become a control character, and as an
    # unescaped SQL pattern the % would be a wildcard. Either way the result would be wrong.
    expected = sql("select count(*) from structures where trim(smiles) ilike '%\\%10%'")
    assert expected > 0, "test data assumption: some SMILES contain the text %10"
    assert len(read_structures_by_smiles("%10", db)) == expected


# I3: % and _ are SQL wildcards and backslash is the escape character; all must be literal.
def test_underscore_is_literal_not_a_wildcard(client, sql):
    assert sql("select count(*) from drug_class where source = 'LEXICOM_'") == 0
    assert client.get(path("drug_class", "source", "LEXICOM_")).status_code == 404
    real = sql("select count(*) from drug_class where trim(source) ilike '%LEXICOMP%'")
    if real:
        assert len(client.get(path("drug_class", "source", "LEXICOMP")).json()) == real


def test_percent_is_literal_not_a_wildcard(client, sql):
    # A value of only "%" would match every row if it were treated as a wildcard.
    expected = sql("select count(*) from drug_class where strpos(source, '%') > 0")
    r = client.get(path("drug_class", "source", "%"))
    if expected == 0:
        assert r.status_code == 404, "a bare % matched rows, so it is still a wildcard"
    else:
        assert len(r.json()) == expected


def test_backslash_in_a_value_is_found(client, sql):
    gene = sql(FIRST_GENE_WITH_BACKSLASH)
    if gene is None:
        pytest.skip("no gene contains a backslash in this release")
    r = client.get(path("target_component", "gene", gene))
    assert r.status_code == 200
    assert any(row["gene"] == gene for row in r.json())


# I4: negative and oversized pagination reached PostgreSQL and failed as a 500.
@pytest.mark.parametrize("query", ["skip=-1&limit=1", "limit=-1", "skip=100000000000000000000&limit=1",
                                   "skip=0&limit=100000000000000000000"])
@pytest.mark.parametrize("route", ["/structures", "/structures/csv", "/pk_az", "/faers/tsv"])
def test_invalid_pagination_is_rejected(client, route, query):
    assert client.get(f"{route}?{query}").status_code == 422


def test_valid_pagination_edges_still_work(client, sql):
    assert client.get("/structures?limit=0").json() == []
    assert client.get("/id_type?limit=1000000").status_code == 200        # at the maximum limit
    assert len(client.get("/id_type?limit=1000000").json()) == sql("select count(*) from id_type")
    assert client.get("/structures?skip=999999&limit=5").json() == []     # beyond the end


# I5: a NUL character cannot be stored in PostgreSQL text and caused a 500.
@pytest.mark.parametrize("route", ["/structures/name/review%00", "/pk_az/type/review%00/csv",
                                   "/faers/meddra_name/x%00y/tsv"])
def test_nul_in_path_is_rejected(client, route):
    r = client.get(route)
    assert r.status_code == 422
    assert r.json() == {"detail": "path contains a NUL character"}


# I6: only three of the four "-class" types have no similarity/confidence.
def test_pld_class_has_confidence_unlike_the_other_class_types(client):
    pld = client.get("/pk_az/type/pld-class").json()
    assert pld and all(row["confidence"] is not None and row["similarity"] is not None for row in pld)
    for name in ("kinase-safety-class", "kinase-selectivity-class", "pfas-class"):
        rows = client.get(f"/pk_az/type/{name}").json()
        assert rows and all(row["confidence"] is None for row in rows)


def test_docs_name_the_types_without_confidence(client):
    description = client.get("/openapi.json").json()["paths"]["/pk_az"]["get"]["description"]
    for name in ("kinase-safety-class", "kinase-selectivity-class", "pfas-class", "pld-class"):
        assert name in description


def test_missing_units_are_reported_as_null(client):
    for name in ("mh-clint", "mppb"):
        rows = client.get(f"/pk_az/type/{name}").json()
        assert rows and all(row["unit"] is None for row in rows)


# I2: known limitation, not yet fixed. This test is expected to fail; if it ever passes,
# the limitation is gone and the note in README.md should be removed.
@pytest.mark.xfail(reason="I2: a path parameter cannot carry an encoded slash", strict=True)
def test_value_containing_a_slash_can_be_looked_up(client, sql):
    gene = sql("select gene from target_component where strpos(gene, '/') > 0 order by id limit 1")
    if gene is None:
        pytest.skip("no gene contains a slash in this release")
    r = client.get(path("target_component", "gene", gene))
    assert r.status_code == 200
    assert any(row["gene"] == gene for row in r.json())
