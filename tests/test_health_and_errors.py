import pytest
from psycopg2.errors import ReadOnlySqlTransaction
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

from app.database import engine
from app.main import app, get_db

UNREACHABLE = "postgresql://user:pass@127.0.0.1:1/none"  # nothing listens on port 1


@pytest.fixture
def use_engine():
    """Serve API requests from sessions bound to a test engine instead of the real one."""
    created = []

    def install(test_engine):
        created.append(test_engine)
        sessions = sessionmaker(bind=test_engine)

        def get_test_db():
            db = sessions()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = get_test_db
        return test_engine

    yield install
    app.dependency_overrides.pop(get_db, None)
    for e in created:
        e.dispose()


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_health_reports_database_and_version(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["database"] == "ok"
    assert body["dbversion"] >= 56


def test_dbversion_returns_the_table_row(client, sql):
    r = client.get("/dbversion")
    assert r.status_code == 200
    version = sql("select max(version) from dbversion")
    dtime = sql("select dtime from dbversion where version = :v", v=version)
    assert r.json() == {"version": version, "dtime": dtime.isoformat()}


def test_api_sessions_are_read_only():
    # Set by the API's own connection options (source "client"), not only by the login's
    # role, so it also holds when the API uses a login that is allowed to write.
    with engine.connect() as conn:
        setting, source = conn.execute(text(
            "select setting, source from pg_settings where name = 'default_transaction_read_only'")).one()
        assert (setting, source) == ("on", "client")
        with pytest.raises(DBAPIError) as e:
            conn.execute(text("create temp table read_only_check (x int)"))
        assert isinstance(e.value.orig, ReadOnlySqlTransaction)


@pytest.mark.parametrize("path", ["/health", "/dbversion", "/structures?limit=1", "/structures/id/5392", "/faers/csv?limit=5"])
def test_unreachable_database_returns_503(client, use_engine, path):
    use_engine(create_engine(UNREACHABLE, connect_args={"connect_timeout": 2}))
    r = client.get(path)
    assert r.status_code == 503
    assert r.json() == {"detail": "Database unavailable"}


def test_root_does_not_depend_on_database(client, use_engine):
    use_engine(create_engine(UNREACHABLE, connect_args={"connect_timeout": 2}))
    assert client.get("/").status_code == 200


def test_query_over_statement_timeout_returns_504(client, use_engine):
    # Same database, but queries are cancelled after 100 ms; this filter scans ~470k rows.
    use_engine(create_engine(engine.url, connect_args={"options": "-c statement_timeout=100"}))
    r = client.get("/faers/meddra_name/a")
    assert r.status_code == 504
    assert r.json() == {"detail": "Database query timed out"}


def test_exhausted_connection_pool_returns_503(client, use_engine):
    small = use_engine(create_engine(engine.url, pool_size=1, max_overflow=0, pool_timeout=0.2))
    held = small.connect()  # occupy the only pooled connection
    try:
        r = client.get("/structures?limit=1")
    finally:
        held.close()
    assert r.status_code == 503
    assert r.json() == {"detail": "Database busy, try again later"}
