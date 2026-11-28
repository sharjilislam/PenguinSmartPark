from fastapi.testclient import TestClient

from app.main import app, reset_demo_lots


def setup_function():
    reset_demo_lots()


def test_system_student_finds_eligible_nearest_lots():
    client = TestClient(app)
    access = client.get("/lots/1/access", params={"user_type": "STUDENT"})
    recommendations = client.post("/recommendations", json={"user_type": "STUDENT", "walking_times": {"1": 3, "2": 6, "3": 1}})
    assert access.json()["allowed"] is True
    assert [lot["lot_id"] for lot in recommendations.json()] == [1, 2]


def test_system_entry_updates_subsequent_recommendation():
    client = TestClient(app)
    event = client.post("/lots/1/events", json={"event_type": "ENTER", "is_ada": False})
    recommendations = client.post("/recommendations", json={"user_type": "STUDENT", "walking_times": {"1": 3, "2": 6, "3": 1}})
    assert event.status_code == 200
    assert event.json()["regular_available"] == 0
    assert [lot["lot_id"] for lot in recommendations.json()] == [2]


def test_system_invalid_event_returns_error_and_preserves_availability():
    client = TestClient(app)
    before = client.get("/lots").json()[0]["regular_available"]
    invalid_event = client.post("/lots/1/events", json={"event_type": "FLY", "is_ada": False})
    after = client.get("/lots").json()[0]["regular_available"]
    assert invalid_event.status_code == 400
    assert invalid_event.json()["detail"] == "Invalid event type"
    assert after == before
