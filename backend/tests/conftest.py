import os

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app import db
from app.auth import attempts
from app.main import app


@pytest.fixture
def database(monkeypatch):
    raw = os.environ.get("TEST_DATABASE_URL")
    assert raw, "TEST_DATABASE_URL is required for integration tests"
    url = make_url(raw)
    assert url.drivername == "postgresql+psycopg" and url.database == "plantly_test"
    engine = create_engine(url)
    monkeypatch.setattr(db, "engine", engine)
    command.upgrade(Config("alembic.ini"), "head")
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(connection, join_transaction_mode="create_savepoint")
        app.dependency_overrides[db.get_db] = lambda: session
        attempts.clear()
        yield session
        app.dependency_overrides.clear()
        session.close()
        transaction.rollback()
    engine.dispose()


@pytest.fixture
def client(database):
    with TestClient(app, base_url="http://localhost:3000") as client:
        yield client


def mutate(client, method, path, **kwargs):
    token = client.get("/api/v1/auth/csrf").json()["csrf_token"]
    return client.request(
        method,
        "/api/v1" + path,
        headers={"Origin": "http://localhost:3000", "X-CSRF-Token": token},
        **kwargs,
    )


def signup(client, email="grower@example.com"):
    response = mutate(
        client, "POST", "/auth/signup", json={"email": email, "password": "a secure test password"}
    )
    assert response.status_code == 201, response.text
    return response.json()
