from app.models.user import User
from app.core.security import verify_password


def test_register_user(client, db_session):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123!",
            "full_name": "Test Student",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test Student"
    assert data["is_active"] is True
    assert "hashed_password" not in data

    user = db_session.query(User).filter(
        User.email == "test@example.com"
    ).first()

    assert user is not None
    assert user.hashed_password != "TestPassword123!"
    assert verify_password("TestPassword123!", user.hashed_password)


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "TestPassword123!",
        "full_name": "Test Student",
    }

    first_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409
    assert second_response.json() == {
        "detail": "Email already registered"
    }


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "TestPassword123!",
            "full_name": "Test Student",
        },
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "student@example.com",
            "password": "123",
            "full_name": "Test Student",
        },
    )

    assert response.status_code == 422