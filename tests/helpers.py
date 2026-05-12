from typing import Any

from httpx import Response
from sqlmodel import Session

from tests.conftest import client, create_user, auth_headers, test_engine
from src.models import User


def create_room_and_add_user_to_room(
    user_id: int, token: str, title: str = "Room"
) -> tuple[int, dict[str, str]]:
    response = client.post(
        "/rooms/",
        json={"title": title},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == title
    assert "id" in response.json()

    room_id = response.json()["id"]
    add_user_to_room(room_id, user_id, token)

    return room_id, response.json()


def get_messages_in_room(room_id: int, token: str, status_code: int = 200) -> Response:
    response = client.get(
        f"/rooms/{room_id}/messages",
        headers=auth_headers(token),
    )

    assert response.status_code == status_code

    return response


def create_message(
    room_id: int, token: str, text: str = "Text", status_code: int = 200
) -> Response:
    response = client.post(
        "/messages",
        json={"room_id": room_id, "text": text},
        headers=auth_headers(token),
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()["text"] == text

    return response


def add_user_to_room(room_id: int, user_id: int, token: str) -> Response:
    response = client.put(
        f"/room_user/{room_id}/users/{user_id}", headers=auth_headers(token)
    )

    assert response.status_code == 200
    return response


def update_message(
    message_id: int, token: str, text: str, status_code: int = 200
) -> None:
    response = client.patch(
        f"/messages/messages/{message_id}",
        json={"text": text},
        headers=auth_headers(token),
    )
    assert response.status_code == status_code


def get_text_message(message_id: int, token: str) -> str:
    response = client.get("/messages", headers=auth_headers(token))
    assert response.status_code == 200

    messages_id_text = {message["id"]: message["text"] for message in response.json()}
    messages_text = messages_id_text.get(message_id)
    assert messages_text is not None

    return messages_text


def delete_message(message_id: int, token: str) -> Response:
    return client.delete(
        f"/messages/{message_id}",
        headers=auth_headers(token),
    )


def get_texts_count_from_messages(
    offset: int = 0, limit: int = 100, order: str = "asc", status_code: int = 200
) -> tuple[list[str], int]:
    user_id, user_token = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id, user_token)
    for i in range(5):
        create_message(room_id, user_token, text=str(i))

    response = client.get(
        f"/rooms/{room_id}/messages?offset={offset}&limit={limit}&order={order}",
        headers=auth_headers(user_token),
    )
    assert response.status_code == status_code
    if status_code == 200:
        texts = [message["text"] for message in response.json()["items"]]
        count = response.json()["total"]

        return texts, count

    return [], 0


def sorting_check(list_in: list[Any], order: str) -> bool:
    list_in_iter = iter(list_in)
    prev = next(list_in_iter)
    for current in list_in_iter:
        if order == "asc":
            if current < prev:
                return False
        elif order == "desc":
            if prev < current:
                return False
        else:
            raise ValueError(f"Invalid order: {order}")

        prev = current
    return True


def sorting_messages_check(order: str) -> None:
    result, count = get_texts_count_from_messages(order=order)
    assert len(result) == count
    assert count > 0
    assert sorting_check(result, order)


def delete_user(user_id: int) -> None:
    with Session(test_engine) as session:
        user = session.get(User, user_id)

        if user is not None:
            session.delete(user)
            session.commit()
