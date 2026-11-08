from datetime import timedelta

import pytest
from conftest import mutate, signup
from sqlalchemy import select

from app.auth import UserSession, now
from app.config import settings

pytestmark = pytest.mark.integration


def test_signup_login_logout_and_csrf(client, database):
    user = signup(client)
    assert client.get("/api/v1/auth/me").json() == user
    row = database.scalar(select(UserSession))
    assert row.token_hash != client.cookies.get(settings.cookie_name)
    assert client.cookies.get(settings.cookie_name)
    assert client.post("/api/v1/auth/logout").status_code == 403
    assert mutate(client, "POST", "/auth/logout").status_code == 204
    assert client.get("/api/v1/auth/me").status_code == 401
    assert (
        mutate(
            client,
            "POST",
            "/auth/login",
            json={"email": "GROWER@example.com", "password": "a secure test password"},
        ).status_code
        == 200
    )
    assert client.get("/api/v1/auth/me").json() == user


@pytest.mark.parametrize("expiry", ["idle", "absolute", "revoked"])
def test_expiration_and_get_does_not_extend_session(client, database, expiry):
    signup(client)
    session = database.scalar(select(UserSession))
    previous = session.last_seen_at
    client.get("/api/v1/auth/me")
    database.refresh(session)
    assert session.last_seen_at == previous
    if expiry == "idle":
        session.last_seen_at = now() - timedelta(hours=13)
    elif expiry == "absolute":
        session.expires_at = now() - timedelta(seconds=1)
    else:
        session.revoked_at = now()
    database.commit()
    assert client.get("/api/v1/auth/me").status_code == 401


def test_preauth_origin_and_validation(client):
    credentials = {"email": "grower@example.com", "password": "a secure test password"}
    assert (
        client.post(
            "/api/v1/auth/signup", json=credentials, headers={"Origin": "http://localhost:3000"}
        ).status_code
        == 403
    )
    token = client.get("/api/v1/auth/csrf").json()["csrf_token"]
    assert (
        client.post(
            "/api/v1/auth/signup",
            json=credentials,
            headers={"Origin": "https://evil.example", "X-CSRF-Token": token},
        ).status_code
        == 403
    )
    assert (
        mutate(client, "POST", "/auth/signup", json={**credentials, "admin": True}).status_code
        == 422
    )
    assert mutate(client, "POST", "/auth/login", json=credentials).status_code == 401


def test_rate_limit(client):
    for _ in range(20):
        client.post(
            "/api/v1/auth/login",
            json={"email": "grower@example.com", "password": "a secure test password"},
        )
    assert (
        client.post(
            "/api/v1/auth/login",
            json={"email": "grower@example.com", "password": "a secure test password"},
        ).status_code
        == 429
    )
