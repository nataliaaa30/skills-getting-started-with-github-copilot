import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(monkeypatch):
    test_activities = {
        "Test Activity": {
            "description": "An activity for API tests",
            "schedule": "Mondays, 3:00 PM",
            "max_participants": 10,
            "participants": [],
        }
    }
    monkeypatch.setattr(app_module, "activities", test_activities)
    return TestClient(app_module.app)


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == {
        "Test Activity": {
            "description": "An activity for API tests",
            "schedule": "Mondays, 3:00 PM",
            "max_participants": 10,
            "participants": [],
        }
    }


def test_signup_adds_participant_to_activity(client):
    response = client.post(
        "/activities/Test%20Activity/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@example.com for Test Activity"
    }
    assert client.get("/activities").json()["Test Activity"]["participants"] == [
        "student@example.com"
    ]
