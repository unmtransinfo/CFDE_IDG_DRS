"""Identifier lookups match exactly (step 16); name and free-text fields stay substring searches.
Each case is checked against the same rule expressed in SQL."""
import pytest

EXACT = "select count(*) from {t} where {c} = :v"
IDENT = "select count(*) from identifier where upper(trim(identifier)) = upper(trim(:v))"
PREFIX = "select count(*) from {t} where {c} like :v || '%'"
PIPE = "select count(*) from act_table_full where upper(:v) = any(string_to_array({c}, '|'))"

# (path, ground-truth SQL, value for the SQL, whether the value must exist)
CASES = [
    ("/structures/inchikey/LIOLIMKSCNQPLV-UHFFFAOYSA-N", EXACT.format(t="structures", c="inchikey"), "LIOLIMKSCNQPLV-UHFFFAOYSA-N", True),
    ("/structures/inchikey/liolimkscnqplv-uhfffaoysa-n", EXACT.format(t="structures", c="inchikey"), "LIOLIMKSCNQPLV-UHFFFAOYSA-N", True),
    ("/structures/inchikey/LIOLIMKSCNQPLV", EXACT.format(t="structures", c="inchikey"), "LIOLIMKSCNQPLV", False),
    ("/target_component/accession/P08581", EXACT.format(t="target_component", c="accession"), "P08581", True),
    ("/target_component/accession/p08581", EXACT.format(t="target_component", c="accession"), "P08581", True),
    ("/target_component/accession/P0", EXACT.format(t="target_component", c="accession"), "P0", False),
    ("/target_component/swissprot/MET_HUMAN", EXACT.format(t="target_component", c="swissprot"), "MET_HUMAN", True),
    ("/target_component/swissprot/MET", EXACT.format(t="target_component", c="swissprot"), "MET", False),
    ("/identifier/identifier/CHEMBL3188267", IDENT, "CHEMBL3188267", True),
    ("/identifier/identifier/chembl3188267", IDENT, "CHEMBL3188267", True),
    ("/identifier/identifier/CHEMBL31882", IDENT, "CHEMBL31882", False),
    ("/atc/code/N02BE01", PREFIX.format(t="atc", c="code"), "N02BE01", True),
    ("/atc/code/N02B", PREFIX.format(t="atc", c="code"), "N02B", True),
    ("/atc/code/n02b", PREFIX.format(t="atc", c="code"), "N02B", True),
    ("/atc/code/02B", PREFIX.format(t="atc", c="code"), "02B", False),
    ("/struct2atc/atc_code/N02BE01", PREFIX.format(t="struct2atc", c="atc_code"), "N02BE01", True),
    ("/product/ndc_product_code/0002-0152", EXACT.format(t="product", c="ndc_product_code"), "0002-0152", True),
    ("/product/ndc_product_code/0002", EXACT.format(t="product", c="ndc_product_code"), "0002", False),
    ("/omop_relationship/umls_cui/C0000737", EXACT.format(t="omop_relationship", c="umls_cui"), "C0000737", True),
    ("/target_go/id/GO:0005737", EXACT.format(t="target_go", c="id"), "GO:0005737", True),
    ("/tdgo2tc/go_id/go:0005737", EXACT.format(t="tdgo2tc", c="go_id"), "GO:0005737", True),
    ("/tdgo2tc/go_id/GO:00057", EXACT.format(t="tdgo2tc", c="go_id"), "GO:00057", False),
    ("/target_keyword/id/KW-0001", EXACT.format(t="target_keyword", c="id"), "KW-0001", True),
    ("/tdkey2tc/tdkey_id/kw-0001", EXACT.format(t="tdkey2tc", c="tdkey_id"), "KW-0001", True),
    ("/act_table_full/accession/P02919", PIPE.format(c="accession"), "P02919", True),
    ("/act_table_full/accession/p02919", PIPE.format(c="accession"), "P02919", True),
    ("/act_table_full/accession/P0291", PIPE.format(c="accession"), "P0291", False),
    ("/act_table_full/swissprot/PBPB_ECOLI", PIPE.format(c="swissprot"), "PBPB_ECOLI", True),
]


def assert_count(client, path, expected):
    r = client.get(path)
    if expected == 0:
        assert r.status_code == 404
    else:
        assert r.status_code == 200
        assert len(r.json()) == expected


@pytest.mark.parametrize(("path", "truth", "value", "exists"), CASES, ids=[c[0] for c in CASES])
def test_lookup_matches_sql(client, sql, path, truth, value, exists):
    expected = sql(truth, v=value)
    assert (expected > 0) == exists, "test data assumption no longer holds"
    assert_count(client, path, expected)


def test_identifier_ignores_case_of_stored_value(client, sql):
    stored = sql("select identifier from identifier where identifier <> upper(identifier) order by id limit 1")
    if stored is None:
        pytest.skip("no lower-case identifiers in this release")
    assert_count(client, f"/identifier/identifier/{stored.strip().upper()}", sql(IDENT, v=stored))


def test_identifier_ignores_spaces_around_stored_value(client, sql):
    stored = sql("select identifier from identifier where identifier <> btrim(identifier) "
                 "and btrim(identifier) ~ '^[A-Za-z0-9._:-]+$' order by id limit 1")
    if stored is None:
        pytest.skip("no space-padded identifiers in this release")
    assert_count(client, f"/identifier/identifier/{stored.strip()}", sql(IDENT, v=stored))


def test_seven_character_cui_in_padded_column(client, sql):
    cui = sql("select umls_cui::text from omop_relationship where length(umls_cui::text) = 7 order by id limit 1")
    if cui is None:
        pytest.skip("no 7-character CUIs in this release")
    assert_count(client, f"/omop_relationship/umls_cui/{cui}", sql(EXACT.format(t="omop_relationship", c="umls_cui"), v=cui))


def test_pipe_list_lookup_returns_multi_component_rows(client):
    rows = client.get("/act_table_full/accession/P02919").json()
    assert all("P02919" in row["accession"].split("|") for row in rows)
    assert any("|" in row["accession"] for row in rows)


def test_atc_percent_is_not_a_wildcard(client):
    assert client.get("/atc/code/N02%25").status_code == 404


def test_name_search_is_still_substring(client):
    names = [row["name"] for row in client.get("/structures/name/capmat").json()]
    assert "capmatinib" in names
