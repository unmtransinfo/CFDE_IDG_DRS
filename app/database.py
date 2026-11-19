import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. Expected postgresql://user:password@host:port/dbname "
        "(see .env.example)."
    )

# Fail fast instead of hanging when the database is unreachable or a query runs away.
CONNECT_TIMEOUT_SECONDS = 5
STATEMENT_TIMEOUT_MS = 30_000

# Every session is read-only, so PostgreSQL rejects writes even when the login is allowed
# to make them. This is a safety net, not a security boundary (a session can turn it off);
# the boundary is a read-only login (db/api_readonly_role.sql).
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": CONNECT_TIMEOUT_SECONDS,
        "options": f"-c statement_timeout={STATEMENT_TIMEOUT_MS} -c default_transaction_read_only=on",
    },
    pool_timeout=10,  # wait at most 10s for a free pooled connection
    pool_pre_ping=True,  # check a pooled connection is alive before using it
    pool_recycle=1800,  # replace connections older than 30 minutes
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
