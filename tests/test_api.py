from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_missing_document():
    response = client.get("/documents/999999")
    assert response.status_code == 404


def test_invalid_create():
    response = client.post("/documents", json={})
    assert response.status_code == 422
