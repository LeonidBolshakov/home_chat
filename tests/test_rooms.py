from conftest import client, create_user, auth_headers


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
    title_1 = "one"
    room_dict_1 = create_room_and_user_in_room(title_1, user_id_1, token_1)

    user_id_2, token_2 = create_user()
    title_2 = "two"
    room_dict_2 = create_room_and_user_in_room(title_2, user_id_2, token_2)

    response = client.get("/rooms", headers=auth_headers(token_1))
    assert response.status_code == 200
    titles = {room["title"] for room in response.json()}
    assert title_1 in titles
    assert title_2 not in titles


def create_room_and_user_in_room(
    title: str, user_id: int, token: str
) -> dict[str, str]:
    response = client.post(
        "/rooms",
        json={
            "title": title,
        },
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    assert response.json()["title"] == title
    assert "id" in response.json()

    room_id = response.json()["id"]
    response = client.put(
        f"/room_user/{room_id}/users/{user_id}", headers=auth_headers(token)
    )
    assert response.status_code == 200

    return response.json()
