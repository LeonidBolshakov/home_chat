from conftest import client, create_user, auth_headers
from httpx import Response


def test_get_rooms_without_token_forbidden() -> None:
    response = client.get("/rooms")
    assert response.status_code in (400, 401)


def test_get_rooms_with_token_success() -> None:
    usaer_id, token = create_user()

    response = client.get("/rooms", headers=auth_headers(token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_rooms_returns_only_rooms_current_user():
    user_id_1, token_1 = create_user()
    room_id_1, room_dict_1 = create_room_and_add_user_to_room(user_id_1, token_1)

    user_id_2, token_2 = create_user()
    room_id_2, room_dict_2 = create_room_and_add_user_to_room(user_id_2, token_2, "two")

    response = client.get("/rooms", headers=auth_headers(token_1))
    assert response.status_code == 200
    ids = {room["id"] for room in response.json()}
    assert room_id_1 in ids
    assert room_id_2 not in ids


def test_delete_room_forbidden_for_non_member():
    user_id_1, user_token_1 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)

    user_id_2, user_token_2 = create_user()
    response = client.delete(f"/rooms/{room_id}", headers=auth_headers(user_token_2))
    assert response.status_code == 403

    response = client.delete(f"/rooms/{room_id}", headers=auth_headers(user_token_1))
    assert response.status_code == 200

    response = client.get(f"/rooms/{room_id}", headers=auth_headers(user_token_1))
    assert response.status_code == 403


def test_post_messages_forbidden_for_non_member():
    user_id_1, user_token_1 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)

    text = "Text"

    user_id_2, user_token_2 = create_user()
    create_message(room_id, text, user_token_2, status_code=403)

    create_message(
        room_id,
        text,
        user_token_1,
    )


def test_get_room_messages_forbidden_for_non_member():
    user_id_1, user_token_1 = create_user()
    user_id_2, user_token_2 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)

    text_message = "Text"
    create_message(room_id, text_message, user_token_1)

    get_messages_in_room(room_id, user_token_2, status_code=403)

    response = get_messages_in_room(room_id, user_token_1)

    messages = response.json()["items"]
    message_texts = {message["text"] for message in messages}
    assert text_message in message_texts


def test_patch_message_forbidden_for_non_author():
    user_id_1, user_token_1 = create_user()
    user_id_2, user_token_2 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)
    add_user_to_room(room_id, user_id_2, user_token_1)

    text_message = "Text"
    response = create_message(room_id, text_message, user_token_1)
    message_id = response.json()["id"]
    update_message(message_id, user_token_2, status_code=403)
    update_message(message_id, user_token_1)


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
    room_id: int, text: str, token: str, status_code: int = 200
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
    message_id: int, token: str, text: str = "_", status_code: int = 200
) -> None:
    response = client.patch(
        f"/messages/messages/{message_id}",
        json={"text": text},
        headers=auth_headers(token),
    )
    assert response.status_code == status_code
