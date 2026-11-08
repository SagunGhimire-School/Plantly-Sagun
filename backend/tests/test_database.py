import os

import pytest
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.db import Base


@pytest.mark.integration
def test_migrations_vector_and_rollback(monkeypatch):
    raw = os.environ.get("TEST_DATABASE_URL")
    assert raw, "TEST_DATABASE_URL is required; use the disposable Compose test-db"
    url = make_url(raw)
    assert url.drivername == "postgresql+psycopg" and url.database == "plantly_test"
    from app import db

    engine = create_engine(url)
    monkeypatch.setattr(db, "engine", engine)
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    command.downgrade(config, "base")
    command.upgrade(config, "head")
    with engine.connect() as conn:
        assert conn.scalar(text("SELECT '[1,2,3]'::vector <-> '[1,2,4]'::vector")) == 1
        assert compare_metadata(MigrationContext.configure(conn), Base.metadata) == []
        conn.execute(text("CREATE TABLE rollback_probe (value integer)"))
        conn.rollback()
        assert conn.scalar(text("SELECT to_regclass('rollback_probe')")) is None
    engine.dispose()
