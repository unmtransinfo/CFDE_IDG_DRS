import csv
import io

import pytest
from sqlalchemy import Integer

from app import models as m

TABLES = [m.ActTableFull, m.Structures, m.Identifier, m.IdType, m.Synonyms, m.TargetClass,
          m.TargetComponent, m.TargetDictionary, m.TargetGo, m.TargetKeyword, m.Td2tc, m.Tdgo2tc,
          m.Tdkey2tc, m.OmopRelationship, m.Product, m.Struct2obprod, m.Atc, m.Struct2atc,
          m.DrugClass, m.Faers, m.FaersFemale, m.FaersMale, m.PkAz]
# Order checks compare in Python, so only tables whose primary key starts with an integer;
# text keys are ordered by the database collation.
INTEGER_KEYED = [t for t in TABLES if isinstance(t.__mapper__.primary_key[0].type, Integer)]


def table_id(model):
    return model.__tablename__


@pytest.mark.parametrize("model", TABLES, ids=table_id)
def test_pages_are_contiguous_and_repeatable(client, model):
    def page(skip, limit):
        return client.get(f"/{model.__tablename__}", params={"skip": skip, "limit": limit}).json()

    first, second, both = page(0, 10), page(10, 10), page(0, 20)
    assert len(both) == 20
    assert first + second == both  # no gaps or repeats between pages
    assert page(0, 20) == both      # same rows, same order, on every call


@pytest.mark.parametrize("model", INTEGER_KEYED, ids=table_id)
def test_pages_follow_primary_key_order(client, model):
    key = model.__mapper__.primary_key[0].name
    values = [row[key] for row in client.get(f"/{model.__tablename__}", params={"limit": 50}).json()]
    assert values == sorted(values)


@pytest.mark.parametrize(("table", "key"), [("structures", "cd_id"), ("faers", "id"), ("pk_az", "struct_id")])
def test_exports_follow_primary_key_order(client, table, key):
    rows = list(csv.DictReader(io.StringIO(client.get(f"/{table}/csv", params={"limit": 200}).text)))
    values = [int(row[key]) for row in rows]
    assert len(values) == 200
    assert values == sorted(values)
