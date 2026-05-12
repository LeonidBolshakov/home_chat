import pytest

from uuid import uuid4

from tests.conftest import create_user, client, auth_headers
from tests.helpers import (
    create_room_and_add_user_to_room,
    get_messages_in_room,
    create_message,
    add_user_to_room,
    update_message,
    get_text_message,
    delete_message,
    get_texts_count_from_messages,
    sorting_messages_check,
)


def test_post_messages_forbidden_for_non_member():
    user_id_1, user_token_1 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)

    user_id_2, user_token_2 = create_user()
    create_message(room_id, user_token_2, status_code=403)

    create_message(room_id, user_token_1)


def test_get_room_messages_forbidden_for_non_member():
    user_id_1, user_token_1 = create_user()
    user_id_2, user_token_2 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)

    text_message = str(uuid4().hex)
    create_message(room_id, user_token_1, text=text_message)

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

    text_old = str(uuid4().hex)
    text_new = str(uuid4().hex)
    response = create_message(room_id, user_token_1, text=text_old)
    message_id = response.json()["id"]

    update_message(message_id, user_token_2, text_new, status_code=403)
    text_message = get_text_message(message_id, user_token_1)
    assert text_message == text_old

    update_message(message_id, user_token_1, text_new)
    text_message = get_text_message(message_id, user_token_1)
    assert text_message == text_new


def test_delete_message_forbidden_for_non_author():
    user_id_1, user_token_1 = create_user()
    user_id_2, user_token_2 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, user_token_1)
    add_user_to_room(room_id, user_id_2, user_token_1)

    text = str(uuid4().hex)
    response = create_message(room_id, user_token_1, text=text)
    message_id = response.json()["id"]

    response = delete_message(message_id, user_token_2)
    assert response.status_code == 403

    assert get_text_message(message_id, user_token_1) == text


def test_delete_message_by_author():
    user_id, user_token = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(user_id, user_token)

    text = str(uuid4().hex)
    response = create_message(room_id, user_token, text=text)
    message_id = response.json()["id"]

    response = delete_message(message_id, user_token)
    assert response.status_code == 200

    response = get_messages_in_room(room_id, user_token)
    assert response.status_code == 200

    messages = response.json()["items"]

    message_ids = [message["id"] for message in messages]

    assert message_id not in message_ids


def test_get_messages_limit():

    texts, _ = get_texts_count_from_messages(limit=2)
    assert texts == ["0", "1"]


def test_get_messages_offset():

    texts, _ = get_texts_count_from_messages(offset=2)
    assert texts == ["2", "3", "4"]


def test_get_messages_limit_offset_and_total():

    texts, count = get_texts_count_from_messages(offset=1, limit=2)

    assert texts == ["1", "2"]
    assert count == 5


def test_get_messages_total_without_pagination():

    texts, count = get_texts_count_from_messages()
    assert len(texts) == 5
    assert count == 5


@pytest.mark.parametrize(
    ("limit", "offset"),
    [
        (0, 0),
        (101, 0),
        (100, -1),
    ],
)
def test_get_messages_validations(limit: int, offset: int):
    get_texts_count_from_messages(
        limit=limit,
        offset=offset,
        status_code=422,
    )


def test_sorting_messages():
    sorting_messages_check("asc")
    sorting_messages_check("desc")


def test_get_messages_returns_only_current_user_messages():
    user_id_1, token_1 = create_user()
    user_id_2, token_2 = create_user()

    room_id, room_dict = create_room_and_add_user_to_room(
        user_id_1,
        token_1,
    )

    add_user_to_room(room_id, user_id_2, token_1)

    text_1 = str(uuid4().hex)
    text_2 = str(uuid4().hex)

    create_message(room_id, token_1, text=text_1)
    create_message(room_id, token_2, text=text_2)

    response = client.get(
        "/messages",
        headers=auth_headers(token_1),
    )

    assert response.status_code == 200

    texts = {message["text"] for message in response.json()}

    assert text_1 in texts
    assert text_2 not in texts


def test_get_messages_without_token_forbidden():
    response = client.get("/messages")

    assert response.status_code in (401, 403)


def test_me_messages_endpoint_empty() -> None:
    user_id, token = create_user()

    response = client.get("/users/me/messages", headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0}
