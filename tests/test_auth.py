import pytest

from uuid import uuid4
from tests.conftest import client, create_user, auth_headers
from tests.helpers import delete_user


def test_login_user_success():
    name = f"u_{uuid4().hex}"
    password = "12345"

    registr_response = client.post(
        "/users/register",
        json={
            "name": name,
            "password": password,
        },
    )
    assert registr_response.status_code == 200

    login_response = client.post(
        "users/login",
        json={
            "name": name,
            "password": password,
        },
    )

    data = login_response.json()
    assert login_response.status_code == 200
    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0


def test_logout_invalidates_token():
    user_id, token = create_user()

    response = client.get("/users/me", headers=auth_headers(token))
    assert response.status_code == 200

    response = client.post("/users/logout", headers=auth_headers(token))
    assert response.status_code == 200

    response = client.get("/users/me", headers=auth_headers(token))
    assert response.status_code == 401


@pytest.mark.parametrize(
    "headers",
    [
        {"Authorization": "Bearer invalid_token"},
        {"Authorization": "invalid"},
        {"Authorization": "Bearer "},
    ],
)
def test_invalid_auth(headers: dict[str, str]) -> None:
    response = client.get("/rooms", headers=headers)
    assert response.status_code == 401


def test_token_for_deleted_user() -> None:
    user_id, user_token = create_user()
    delete_user(user_id)
    response = client.get("/rooms", headers=auth_headers(user_token))
    assert response.status_code == 401


def test_login_missing_user() -> None:
    response = client.post(
        "/users/login",
        json={"name": f"missing_{uuid4().hex}", "password": "bad"},
    )
    assert response.status_code == 401
