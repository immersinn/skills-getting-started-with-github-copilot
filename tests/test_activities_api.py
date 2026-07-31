def test_root_redirects_to_static_index(client):
    # Arrange
    root_path = "/"

    # Act
    response = client.get(root_path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data(client):
    # Arrange
    activities_path = "/activities"

    # Act
    response = client.get(activities_path)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]
    assert isinstance(payload["Chess Club"]["participants"], list)


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {student_email} for {activity_name}"

    updated_activities = client.get("/activities").json()
    assert student_email in updated_activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {student_email} from {activity_name}"

    updated_activities = client.get("/activities").json()
    assert student_email not in updated_activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    student_email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "not.signed.up@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": student_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
