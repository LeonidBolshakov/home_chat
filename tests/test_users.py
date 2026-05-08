from uuid import uuid4
from tests.conftest import client, create_user, auth_headers


def test_pytest_works():
    response = client.get("/docs")

    assert response.status_code == 200


def test_get_users_me_without_token_is_forbiden():
    response = client.get("/users/me")

    assert response.status_code in (401, 403)


def test_register_user_success():
    name = f"u_{uuid4().hex}"
    response = client.post(
        "/users/register",
        json={
            "name": name,
            "password": "12345",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name
    assert "id" in data


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
    name, token = create_user()

    response = client.get("/users/me", headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["name"] == name

    response = client.post("/users/logout", headers=auth_headers(token))
    assert response.status_code == 200

    response = client.get("/users/me", headers=auth_headers(token))
    assert response.status_code == 401
