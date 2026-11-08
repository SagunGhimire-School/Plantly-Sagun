import pytest
from fastapi.testclient import TestClient

from app.ai import GeminiAdapter, PlanningUnavailable
from app.main import app


def test_liveness_and_unconfigured_ai():
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/v1/capabilities").json()["planning"]["available"] is False
    with pytest.raises(PlanningUnavailable):
        GeminiAdapter().generate("must not call provider")


def test_body_limit():
    response = TestClient(app).post("/api/v1/auth/login", content=b"x" * 65537)
    assert response.status_code == 413
