from tests.conftest import client, create_user, auth_headers
from tests.helpers import create_room_and_add_user_to_room, add_user_to_room


def test_get_rooms_without_token_forbidden() -> None:
    response = client.get("/rooms")
    assert response.status_code in (400, 401)


def test_get_rooms_with_token_success() -> None:
    user_id, token = create_user()

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


def test_get_users_by_room_allows_members_and_forbids_non_members():

    user_id_1, token_1 = create_user()
    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, token_1)
    user_id_3, token_3 = create_user()

    response = client.get(f"/rooms/{room_id}/users", headers=auth_headers(token_1))
    assert response.status_code == 200

    response = client.get(f"/rooms/{room_id}/users", headers=auth_headers(token_3))
    assert response.status_code == 403


def test_get_users_by_room_returns_only_room_members():

    user_id_1, token_1 = create_user()
    room_id, room_dict = create_room_and_add_user_to_room(user_id_1, token_1)
    user_id_2, token_2 = create_user()
    user_id_3, token_3 = create_user()
    add_user_to_room(room_id, user_id_2, token_1)

    response = client.get(f"/rooms/{room_id}/users", headers=auth_headers(token_1))
    assert response.status_code == 200

    room_member_ids = {user["id"] for user in response.json()}
    assert room_member_ids == {user_id_1, user_id_2}
    assert user_id_3 not in room_member_ids


def test_room_get_update_success() -> None:
    user_id, token = create_user()
    room_id, room_dict = create_room_and_add_user_to_room(user_id, token)

    response = client.get(f"/rooms/{room_id}", headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json()["id"] == room_id

    response = client.patch(
        f"/rooms/{room_id}",
        json={"title": "Renamed"},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Renamed"


def test_room_delete_not_found_room_forbidden() -> None:
    user_id, token = create_user()
    room_id, room_dict = create_room_and_add_user_to_room(user_id, token)

    response = client.delete("/rooms/999", headers=auth_headers(token))
    assert response.status_code == 404
