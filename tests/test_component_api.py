from fastapi.testclient import TestClient

from app.main import app, reset_demo_lots


def setup_function():
    reset_demo_lots()


def test_component_api_returns_healthy_status():
    response = TestClient(app).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_component_api_combines_lot_lookup_and_access_check():
    response = TestClient(app).get("/lots/1/access", params={"user_type": "STUDENT"})
    assert response.status_code == 200
    assert response.json()["allowed"] is True


def test_component_api_returns_error_for_unknown_lot():
    response = TestClient(app).get("/lots/99/access", params={"user_type": "STUDENT"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Parking lot not found"
