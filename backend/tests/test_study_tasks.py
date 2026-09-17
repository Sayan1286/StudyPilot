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


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def create_study_plan(client, token, title="Python Study Plan"):
    today = datetime.now(timezone.utc).date()

    response = client.post(
        "/study-plans",
        json={
            "title": title,
            "subject": "Python",
            "goal": "Build a strong Python foundation",
            "start_date": today.isoformat(),
            "end_date": (today + timedelta(days=30)).isoformat(),
            "daily_hours": 2.0,
        },
        headers=auth_header(token),
    )

    assert response.status_code == 201

    return response.json()["id"]


def study_task_payload():
    return {
        "title": "Learn Python functions",
        "description": "Study functions, parameters, and return values.",
       "scheduled_date": datetime.now(timezone.utc).date().isoformat(),
        "estimated_minutes": 60,
    }


def test_create_study_task(client):
    token = register_and_login(
        client,
        "student1@example.com",
        "Student One",
    )

    study_plan_id = create_study_plan(client, token)

    response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=study_task_payload(),
        headers=auth_header(token),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["study_plan_id"] == study_plan_id
    assert data["title"] == "Learn Python functions"
    assert data["description"] == (
        "Study functions, parameters, and return values."
    )
    assert data["estimated_minutes"] == 60
    assert data["status"] == "pending"


def test_list_study_tasks(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    study_plan_id = create_study_plan(client, token)

    first_payload = study_task_payload()

    second_payload = study_task_payload()
    second_payload["title"] = "Practice Python functions"
    second_payload["scheduled_date"] = (
        datetime.now(timezone.utc).date() + timedelta(days=1)
    ).isoformat()

    first_response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=first_payload,
        headers=auth_header(token),
    )

    second_response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=second_payload,
        headers=auth_header(token),
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get(
        f"/study-plans/{study_plan_id}/tasks",
        headers=auth_header(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Learn Python functions"
    assert data[1]["title"] == "Practice Python functions"


def test_get_study_task(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    study_plan_id = create_study_plan(client, token)

    create_response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=study_task_payload(),
        headers=auth_header(token),
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/study-plans/{study_plan_id}/tasks/{task_id}",
        headers=auth_header(token),
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_user_cannot_create_task_in_another_users_plan(client):
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

    study_plan_id = create_study_plan(client, token_one)

    response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=study_task_payload(),
        headers=auth_header(token_two),
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Study plan not found"}


def test_user_cannot_access_another_users_task(client):
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

    study_plan_id = create_study_plan(client, token_one)

    create_response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=study_task_payload(),
        headers=auth_header(token_one),
    )

    task_id = create_response.json()["id"]

    response = client.get(
        f"/study-plans/{study_plan_id}/tasks/{task_id}",
        headers=auth_header(token_two),
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Study task not found"}


def test_update_study_task(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    study_plan_id = create_study_plan(client, token)

    create_response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=study_task_payload(),
        headers=auth_header(token),
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/study-plans/{study_plan_id}/tasks/{task_id}",
        json={
            "title": "Master Python functions",
            "estimated_minutes": 90,
            "status": "completed",
        },
        headers=auth_header(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Master Python functions"
    assert data["estimated_minutes"] == 90
    assert data["status"] == "completed"
    assert data["description"] == (
        "Study functions, parameters, and return values."
    )


def test_delete_study_task(client):
    token = register_and_login(
        client,
        "student@example.com",
        "Student",
    )

    study_plan_id = create_study_plan(client, token)

    create_response = client.post(
        f"/study-plans/{study_plan_id}/tasks",
        json=study_task_payload(),
        headers=auth_header(token),
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/study-plans/{study_plan_id}/tasks/{task_id}",
        headers=auth_header(token),
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/study-plans/{study_plan_id}/tasks/{task_id}",
        headers=auth_header(token),
    )

    assert get_response.status_code == 404


def test_study_tasks_require_authentication(client):
    response = client.get(
        "/study-plans/00000000-0000-0000-0000-000000000000/tasks"
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}