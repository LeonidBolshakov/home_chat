from uuid import uuid4
from tests.conftest import client

from tests.conftest import create_user, auth_headers


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


def test_users_list_and_duplicate_register_errors() -> None:
    user_id, token = create_user()

    response = client.get("/users", headers=auth_headers(token))
    assert response.status_code == 200
    assert user_id in {user["id"] for user in response.json()}

    name = f"u_{uuid4().hex}"
    response = client.post("/users/register", json={"name": name, "password": "12345"})
    assert response.status_code == 200

    response = client.post("/users/register", json={"name": name, "password": "12345"})
    assert response.status_code == 409
