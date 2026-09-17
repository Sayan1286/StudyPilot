from datetime import datetime, timedelta, timezone


def register_and_login(client, email, full_name):
    password = "TestPassword123!"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": full_name,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def study_plan_payload():
    today = datetime.now(timezone.utc).date()

    return {
        "title": "Python Study Plan",
        "subject": "Python",
        "goal": "Build a strong Python foundation",
        "start_date": today.isoformat(),
        "end_date": (today + timedelta(days=30)).isoformat(),
        "daily_hours": 2.0,
    }


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_create_study_plan(client):
    token = register_and_login(
        client,
        "student1@example.com",
        "Student One",
    )

    response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Python Study Plan"
    assert data["subject"] == "Python"
    assert data["goal"] == "Build a strong Python foundation"
    assert data["daily_hours"] == 2.0
    assert data["status"] == "active"
    assert data["user_id"]


def test_list_study_plans_only_returns_current_users_plans(client):
    token_one = register_and_login(
        client,
        "student1@example.com",
        "Student One",
    )

    token_two = register_and_login(
        client,
        "student2@example.com",
        "Student Two",
    )

    first_response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token_one),
    )

    assert first_response.status_code == 201

    second_payload = study_plan_payload()
    second_payload["title"] = "SQL Study Plan"

    second_response = client.post(
        "/study-plans",
        json=second_payload,
        headers=auth_header(token_two),
    )

    assert second_response.status_code == 201

    response = client.get(
        "/study-plans",
        headers=auth_header(token_one),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Python Study Plan"


def test_get_study_plan(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    create_response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token),
    )

    study_plan_id = create_response.json()["id"]

    response = client.get(
        f"/study-plans/{study_plan_id}",
        headers=auth_header(token),
    )

    assert response.status_code == 200
    assert response.json()["id"] == study_plan_id


def test_user_cannot_access_another_users_study_plan(client):
    token_one = register_and_login(
        client,
        "student1@example.com",
        "Student One",
    )

    token_two = register_and_login(
        client,
        "student2@example.com",
        "Student Two",
    )

    create_response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token_one),
    )

    study_plan_id = create_response.json()["id"]

    response = client.get(
        f"/study-plans/{study_plan_id}",
        headers=auth_header(token_two),
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Study plan not found"}


def test_update_study_plan(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    create_response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token),
    )

    study_plan_id = create_response.json()["id"]

    response = client.put(
        f"/study-plans/{study_plan_id}",
        json={
            "title": "Advanced Python Study Plan",
            "daily_hours": 3.0,
        },
        headers=auth_header(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Advanced Python Study Plan"
    assert data["daily_hours"] == 3.0
    assert data["subject"] == "Python"


def test_update_study_plan_rejects_invalid_dates(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    create_response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token),
    )

    study_plan_id = create_response.json()["id"]

    response = client.put(
        f"/study-plans/{study_plan_id}",
        json={
            "start_date": "2030-01-01",
            "end_date": "2029-01-01",
        },
        headers=auth_header(token),
    )

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert isinstance(data["detail"], list)
    assert any(
        "end_date must be on or after start_date" in error["msg"]
        for error in data["detail"]
    )


def test_delete_study_plan(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    create_response = client.post(
        "/study-plans",
        json=study_plan_payload(),
        headers=auth_header(token),
    )

    study_plan_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/study-plans/{study_plan_id}",
        headers=auth_header(token),
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/study-plans/{study_plan_id}",
        headers=auth_header(token),
    )

    assert get_response.status_code == 404


def test_study_plans_require_authentication(client):
    response = client.get("/study-plans")

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}