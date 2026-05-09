from fastapi.testclient import TestClient
from uuid import uuid4
from sqlmodel import create_engine, SQLModel, Session

from src.db import get_session
from src.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SQLModel.metadata.create_all(test_engine)


def get_test_sessin():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_sessin

client = TestClient(app)


def register_user(name: str, password: str = "12345"):
    return client.post(
        "users/register",
        json={
            "name": name,
            "password": password,
        },
    )


def login_service(name: str, password: str = "12345"):
    return client.post(
        "users/login",
        json={
            "name": name,
            "password": password,
        },
    )


def create_user(password: str = "12345") -> tuple[int, str]:
    name = f"u_{uuid4().hex}"
    response = register_user(name, password)
    assert response.status_code == 200
    assert response.json().get("id") is not None
    user_id = response.json()["id"]

    response = login_service(name, password)
    assert response.status_code == 200

    token = response.json().get("access_token")
    return user_id, token


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
