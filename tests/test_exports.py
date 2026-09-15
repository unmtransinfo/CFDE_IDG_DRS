import csv
import io

import pytest

from app import models as m

# Tables with /csv and /tsv exports, and columns each export leaves out.
EXPORTS = [(m.ActTableFull, ()), (m.Structures, ("molfile",)), (m.Synonyms, ()), (m.TargetComponent, ()),
           (m.Product, ()), (m.Faers, ()), (m.FaersFemale, ()), (m.FaersMale, ()), (m.PkAz, ())]
DELIMITER = {"csv": ",", "tsv": "\t"}


def parse(text, fmt):
    return list(csv.reader(io.StringIO(text), delimiter=DELIMITER[fmt]))


@pytest.mark.parametrize("fmt", ["csv", "tsv"])
@pytest.mark.parametrize(("model", "excluded"), EXPORTS, ids=[t.__tablename__ for t, _ in EXPORTS])
def test_export_headers_rows_and_download_name(client, model, excluded, fmt):
    table = model.__tablename__
    r = client.get(f"/{table}/{fmt}", params={"limit": 25})
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv" if fmt == "csv" else "text/tab-separated-values")
    disposition = r.headers["content-disposition"]
    assert f"filename=drugcentral_{table}_" in disposition and disposition.endswith(f".{fmt}")

    rows = parse(r.text, fmt)
    header = [c.key for c in model.__mapper__.columns if c.key not in excluded]
    assert rows[0] == header
    assert len(rows) == 26
    assert all(len(row) == len(header) for row in rows)  # quoting keeps commas/tabs inside fields
    # QUOTE_NONNUMERIC: numbers are written unquoted (every export starts with an integer key)
    assert r.text.splitlines()[1][0].isdigit()


@pytest.mark.parametrize("fmt", ["csv", "tsv"])
def test_filtered_exports_match_json(client, sql, fmt):
    struct_id = sql("select struct_id from faers_female where struct_id in (select struct_id from faers_male) "
                    "and struct_id in (select struct_id from faers) order by struct_id limit 1")
    for path in (f"/faers/struct_id/{struct_id}", f"/faers_female/struct_id/{struct_id}",
                 f"/faers_male/struct_id/{struct_id}", "/pk_az/struct_id/4", "/pk_az/type/herg"):
        json_rows = client.get(path).json()
        export_rows = parse(client.get(f"{path}/{fmt}").text, fmt)
        assert len(export_rows) - 1 == len(json_rows) > 0, path


def test_structures_export_leaves_out_multiline_molfile(client):
    header = parse(client.get("/structures/csv", params={"limit": 1}).text, "csv")[0]
    assert "molfile" not in header and "smiles" in header
