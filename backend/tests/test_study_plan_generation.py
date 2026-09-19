from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.schemas.study_plan_generation import StudyPlanGenerationRequest
from app.services.study_plan_generation import LocalStudyPlanGenerator


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

def build_request(
    start_date=None,
    end_date=None,
):
    today = datetime.now(timezone.utc).date()

    return StudyPlanGenerationRequest(
        subject="Python",
        goal="Build a strong Python foundation",
        available_hours_per_day=2.0,
        start_date=start_date or today,
        end_date=end_date or today + timedelta(days=2),
    )


def test_local_generator_creates_one_task_per_day():
    request = build_request()

    generator = LocalStudyPlanGenerator()
    response = generator.generate(request)

    assert len(response.tasks) == 3


def test_local_generator_uses_daily_hours_for_task_duration():
    request = build_request()

    generator = LocalStudyPlanGenerator()
    response = generator.generate(request)

    assert all(task.estimated_minutes == 120 for task in response.tasks)


def test_local_generator_preserves_request_information():
    request = build_request()

    generator = LocalStudyPlanGenerator()
    response = generator.generate(request)

    assert response.subject == "Python"
    assert response.goal == "Build a strong Python foundation"
    assert response.daily_hours == 2.0
    assert response.start_date == request.start_date
    assert response.end_date == request.end_date


def test_generation_request_rejects_invalid_dates():
    today = datetime.now(timezone.utc).date()

    with pytest.raises(ValidationError):
        StudyPlanGenerationRequest(
            subject="Python",
            goal="Learn Python",
            available_hours_per_day=2.0,
            start_date=today + timedelta(days=5),
            end_date=today,
        )


def test_generation_request_rejects_period_over_365_days():
    today = datetime.now(timezone.utc).date()

    with pytest.raises(ValidationError):
        StudyPlanGenerationRequest(
            subject="Python",
            goal="Learn Python",
            available_hours_per_day=2.0,
            start_date=today,
            end_date=today + timedelta(days=365),
        )


def test_generation_request_rejects_more_than_24_hours_per_day():
    today = datetime.now(timezone.utc).date()

    with pytest.raises(ValidationError):
        StudyPlanGenerationRequest(
            subject="Python",
            goal="Learn Python",
            available_hours_per_day=25.0,
            start_date=today,
            end_date=today + timedelta(days=7),
        )
def test_generate_study_plan_requires_authentication(client):
    response = client.post(
        "/study-plans/generate",
        json={
            "subject": "Python",
            "goal": "Build a strong Python foundation",
            "available_hours_per_day": 2.0,
            "start_date": "2026-09-20",
            "end_date": "2026-09-22",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_generate_study_plan_endpoint(client):
    token = register_and_login(
        client,
        "generator@example.com",
        "Generator Student",
    )

    response = client.post(
        "/study-plans/generate",
        json={
            "subject": "Python",
            "goal": "Build a strong Python foundation",
            "available_hours_per_day": 2.0,
            "start_date": "2026-09-20",
            "end_date": "2026-09-22",
        },
        headers=auth_header(token),
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Python Study Plan"
    assert data["subject"] == "Python"
    assert data["goal"] == "Build a strong Python foundation"
    assert data["daily_hours"] == 2.0
    assert data["start_date"] == "2026-09-20"
    assert data["end_date"] == "2026-09-22"
    assert len(data["tasks"]) == 3

    assert data["tasks"][0]["scheduled_date"] == "2026-09-20"
    assert data["tasks"][1]["scheduled_date"] == "2026-09-21"
    assert data["tasks"][2]["scheduled_date"] == "2026-09-22"