import os
from concurrent.futures import ThreadPoolExecutor

import pytest
from conftest import mutate, signup
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.auth import User
from app.db import get_db
from app.growing import Plot
from app.main import app

pytestmark = pytest.mark.integration
INPUT = {
    "plot_name": "Back garden",
    "area_m2": "12.5",
    "region": "Central Texas",
    "season_label": "Spring",
    "year": 2027,
}


def test_draft_resume_revision_and_atomic_completion(client, database):
    signup(client)
    assert client.get("/api/v1/onboarding/draft").json()["revision"] == 0
    saved = mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 0, "step": 1, "draft_data": {"plot_name": "Back garden"}},
    )
    assert saved.status_code == 200
    assert saved.json()["draft_data"]["soil_ph"] is None
    assert (
        mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 1}).status_code
        == 422
    )
    assert database.scalar(select(func.count()).select_from(Plot)) == 0
    assert (
        mutate(
            client,
            "PUT",
            "/onboarding/draft",
            json={"expected_revision": 0, "step": 1, "draft_data": INPUT},
        ).status_code
        == 409
    )
    saved = mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 1, "step": 3, "draft_data": INPUT},
    )
    assert saved.json()["revision"] == 2
    mutate(client, "POST", "/auth/logout")
    mutate(
        client,
        "POST",
        "/auth/login",
        json={"email": "grower@example.com", "password": "a secure test password"},
    )
    assert client.get("/api/v1/onboarding/draft").json()["draft_data"]["plot_name"] == "Back garden"
    result = mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 2})
    assert result.status_code == 200
    assert (
        mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 2}).json()
        == result.json()
    )
    assert (
        mutate(
            client,
            "PUT",
            "/onboarding/draft",
            json={"expected_revision": 2, "step": 3, "draft_data": INPUT},
        ).json()["status"]
        == "completed"
    )
    assert database.scalar(select(func.count()).select_from(Plot)) == 1
    context = client.get("/api/v1/dashboard").json()["contexts"][0]
    assert context["inputs"]["soil_observation"]["ph"] is None
    assert context["inputs"]["soil_observation"]["source_type"] == "unknown"
    assert context["budget_amount"] is None
    assert (
        mutate(client, "POST", f"/plots/{result.json()['plot_id']}/plan-generations").status_code
        == 503
    )


def test_other_grower_cannot_read_records_or_draft(client, database):
    signup(client)
    mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 0, "step": 3, "draft_data": INPUT},
    )
    ids = mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 1}).json()
    with TestClient(app, base_url="http://localhost:3000") as other:
        signup(other, "other@example.com")
        assert other.get("/api/v1/plots").json() == []
        assert other.get("/api/v1/seasons").json() == []
        assert other.get("/api/v1/onboarding/draft").json()["revision"] == 0
        assert other.get(f"/api/v1/plots/{ids['plot_id']}").status_code == 404
        assert other.get(f"/api/v1/dashboard?plot_id={ids['plot_id']}").status_code == 404
        assert mutate(other, "POST", f"/plots/{ids['plot_id']}/plan-generations").status_code == 404


@pytest.mark.parametrize(
    "changes",
    [
        {"area_m2": -1},
        {"soil_ph": 8},
        {"soil_ph": 15, "soil_observed_on": "2026-01-01"},
        {"budget_amount": 10},
        {"start_date": "2027-03-01", "end_date": "2027-01-01"},
        {"soil_ph": 6, "soil_observed_on": "2200-01-01"},
        {"verified": True},
    ],
)
def test_invalid_input_keeps_existing_draft(client, changes):
    signup(client)
    response = mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 0, "step": 2, "draft_data": {**INPUT, **changes}},
    )
    assert response.status_code == 422
    assert client.get("/api/v1/onboarding/draft").json()["revision"] == 0


def test_user_reported_provenance_and_new_plot(client, database):
    signup(client)
    values = {
        **INPUT,
        "soil_ph": "6.5",
        "soil_observed_on": "2026-01-01",
        "soil_method": "home meter",
        "budget_amount": "0",
        "currency": "USD",
    }
    mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 0, "step": 3, "draft_data": values},
    )
    mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 1})
    record = client.get("/api/v1/dashboard").json()["contexts"][0]
    assert record["inputs"]["soil_observation"]["scientifically_verified"] is False
    assert record["inputs"]["soil_observation"]["source_type"] == "user_reported"
    assert record["budget_amount"] == "0.00"
    assert (
        mutate(
            client,
            "PUT",
            "/onboarding/draft",
            json={"expected_revision": 1, "step": 3, "draft_data": INPUT},
        ).status_code
        == 409
    )
    assert (
        mutate(
            client,
            "PUT",
            "/onboarding/draft",
            json={"expected_revision": 1, "step": 3, "draft_data": INPUT, "start_new": True},
        ).status_code
        == 200
    )
    mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 2})
    assert database.scalar(select(func.count()).select_from(Plot)) == 2


def test_concurrent_draft_saves_use_real_transactions(database):
    # Dedicated committed account on the guarded disposable DB allows two independent connections.
    engine = create_engine(os.environ["TEST_DATABASE_URL"])

    def independent_db():
        with Session(engine) as session:
            yield session

    previous = app.dependency_overrides[get_db]
    app.dependency_overrides[get_db] = independent_db
    account_id = None
    try:
        with TestClient(app, base_url="http://localhost:3000") as client:
            account = signup(client, "concurrent@example.com")
            account_id = account["id"]
            token = client.get("/api/v1/auth/csrf").json()["csrf_token"]
            cookies = dict(client.cookies)

        def save(name):
            with TestClient(app, base_url="http://localhost:3000") as browser:
                browser.cookies.update(cookies)
                return browser.put(
                    "/api/v1/onboarding/draft",
                    headers={"Origin": "http://localhost:3000", "X-CSRF-Token": token},
                    json={"expected_revision": 0, "step": 1, "draft_data": {"plot_name": name}},
                ).status_code

        with ThreadPoolExecutor(max_workers=2) as pool:
            assert sorted(pool.map(save, ["A", "B"])) == [200, 409]
    finally:
        app.dependency_overrides[get_db] = previous
        if account_id:
            import uuid

            with Session(engine) as session:
                session.delete(session.get(User, uuid.UUID(account_id)))
                session.commit()
        engine.dispose()


def test_shared_season_revision_edit_and_account_deletion(client, database):
    signup(client)
    mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 0, "step": 3, "draft_data": INPUT},
    )
    ids = mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 1}).json()
    second = {
        "plot_name": "Bed two",
        "area_m2": "5",
        "region": "Central Texas",
        "season_id": ids["season_id"],
    }
    assert (
        mutate(
            client,
            "PUT",
            "/onboarding/draft",
            json={"expected_revision": 1, "step": 3, "draft_data": second, "start_new": True},
        ).status_code
        == 200
    )
    assert (
        mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 2}).status_code
        == 200
    )
    assert len(client.get("/api/v1/seasons").json()) == 1
    assert len(client.get("/api/v1/plots").json()) == 2
    update = {
        "expected_revision": 1,
        "name": "Renamed plot",
        "area_m2": "16",
        "region": "Central Texas",
    }
    assert mutate(client, "PATCH", f"/plots/{ids['plot_id']}", json=update).json()["revision"] == 2
    assert mutate(client, "PATCH", f"/plots/{ids['plot_id']}", json=update).status_code == 409
    assert mutate(client, "DELETE", "/auth/me").status_code == 204
    assert client.get("/api/v1/auth/me").status_code == 401
    assert database.scalar(select(func.count()).select_from(Plot)) == 0


def test_cannot_attach_another_owners_season(client, database):
    signup(client)
    mutate(
        client,
        "PUT",
        "/onboarding/draft",
        json={"expected_revision": 0, "step": 3, "draft_data": INPUT},
    )
    ids = mutate(client, "POST", "/onboarding/complete", json={"expected_revision": 1}).json()
    with TestClient(app, base_url="http://localhost:3000") as other:
        signup(other, "another@example.com")
        mutate(
            other,
            "PUT",
            "/onboarding/draft",
            json={
                "expected_revision": 0,
                "step": 3,
                "draft_data": {**INPUT, "season_id": ids["season_id"]},
            },
        )
        assert (
            mutate(other, "POST", "/onboarding/complete", json={"expected_revision": 1}).status_code
            == 404
        )
