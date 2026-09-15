"""Integration tests: the API runs in-process (FastAPI TestClient) against the database in
DATABASE_URL, taken from the environment or the repo's .env. They expect DrugCentral
dbversion 56 or newer (pk_az is new in 56), e.g. the local copy that
scripts/restore_local_db.sh creates."""
from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")  # never overrides an existing DATABASE_URL

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import text  # noqa: E402

from app.database import engine  # noqa: E402
from app.main import app  # noqa: E402

MIN_DBVERSION = 56


def pytest_sessionstart(session):
    try:
        with engine.connect() as conn:
            version = conn.execute(text("select max(version) from dbversion")).scalar()
    except Exception as e:  # any connection problem is reported the same way
        pytest.exit(f"Cannot query the database in DATABASE_URL: {e}", returncode=2)
    if version < MIN_DBVERSION:
        pytest.exit(f"Tests expect DrugCentral dbversion >= {MIN_DBVERSION}; this database is {version}.", returncode=2)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def sql():
    """Run a scalar SQL query against the same database, for ground-truth values."""
    def run(query, **params):
        with engine.connect() as conn:
            return conn.execute(text(query), params).scalar()
    return run
