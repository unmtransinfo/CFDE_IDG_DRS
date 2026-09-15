import pytest

CLASS_TYPES = ["kinase-safety-class", "kinase-selectivity-class", "pfas-class"]


def test_all_predictions_for_one_drug(client, sql):
    rows = client.get("/pk_az/struct_id/4").json()
    assert len(rows) == sql("select count(*) from pk_az where struct_id = 4") == 25
    assert all(row["struct_id"] == 4 for row in rows)
    assert [row["type"] for row in rows] == sorted(row["type"] for row in rows)


@pytest.mark.parametrize("prop", ["herg", "HERG", "solubility-dd", *CLASS_TYPES])
def test_type_lookup_is_exact_and_case_insensitive(client, sql, prop):
    rows = client.get(f"/pk_az/type/{prop}").json()
    assert len(rows) == sql("select count(*) from pk_az where type = lower(:t)", t=prop) > 0
    assert {row["type"] for row in rows} == {prop.lower()}


@pytest.mark.parametrize("path", ["/pk_az/type/her", "/pk_az/type/not-a-type", "/pk_az/struct_id/-1"])
def test_unknown_values_return_404(client, path):
    assert client.get(path).status_code == 404


@pytest.mark.parametrize("prop", CLASS_TYPES)
def test_class_types_have_no_similarity_or_confidence(client, prop):
    rows = client.get(f"/pk_az/type/{prop}").json()
    assert rows and all(row["similarity"] is None and row["confidence"] is None for row in rows)


def test_kinase_class_value_counts_listed_kinases(client):
    for prop in ("kinase-safety-class", "kinase-selectivity-class"):
        for row in client.get(f"/pk_az/type/{prop}").json():
            assert row["value"] == len(row["description"].split(","))


def test_confidence_matches_similarity_bands(client):
    for row in client.get("/pk_az/type/herg").json():
        assert row["confidence"] == ("High" if row["similarity"] >= 0.8 else "Moderate")
        assert row["similarity"] >= 0.65


def test_docs_describe_pk_az(client):
    spec = client.get("/openapi.json").json()
    assert "AstraZeneca" in spec["paths"]["/pk_az"]["get"]["description"]
    assert sum(path.startswith("/pk_az") for path in spec["paths"]) == 9
