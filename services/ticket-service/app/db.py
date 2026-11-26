"""Database connection. MySQL when MYSQL_HOST is set, otherwise a test database in memory."""
import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

MYSQL_HOST = os.getenv("MYSQL_HOST")

if MYSQL_HOST:
    url = (
        f"mysql+pymysql://{os.environ['MYSQL_USER']}:{os.environ['MYSQL_PASSWORD']}"
        f"@{MYSQL_HOST}:{os.getenv('MYSQL_PORT', '3306')}/{os.getenv('MYSQL_DATABASE', 'transit')}"
    )
    engine = create_engine(url, pool_pre_ping=True)
else:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                           poolclass=StaticPool)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create the tables. MySQL can need a minute to start, so try for up to 2 minutes."""
    from . import models  # noqa: F401

    for attempt in range(60):
        try:
            Base.metadata.create_all(engine)
            return
        except Exception as error:
            print(f"Database not ready yet ({attempt + 1}/60): {error}", flush=True)
            time.sleep(2)
    raise RuntimeError("Database never became ready")
