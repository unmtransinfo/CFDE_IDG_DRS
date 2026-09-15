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

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": CONNECT_TIMEOUT_SECONDS,
        "options": f"-c statement_timeout={STATEMENT_TIMEOUT_MS}",
    },
    pool_pre_ping=True,  # check a pooled connection is alive before using it
    pool_recycle=1800,  # replace connections older than 30 minutes
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
