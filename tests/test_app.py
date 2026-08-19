from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_list():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_rejects_duplicate_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_when_activity_is_full():
    activity_name = "Test Activity"
    activities[activity_name] = {
        "description": "Temporary activity",
        "schedule": "Mondays, 4:00 PM",
        "max_participants": 1,
        "participants": ["first@mergington.edu"],
    }

    response = client.post(f"/activities/{activity_name}/signup?email=second@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"

    del activities[activity_name]


def test_delete_signup_removes_participant():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]

    activities[activity_name]["participants"].append(email)
