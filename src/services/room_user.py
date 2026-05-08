from sqlmodel import Session

from src.models import RoomUser
from src.crud.room_user import (
    create_room_user,
    get_rooms_users,
    is_user_in_room,
    delete_users_from_room,
    delete_user_from_room,
    count_users_in_room,
)
from src.crud.rooms import get_room_by_id
from src.crud.users import get_user_by_id
from src.errors import (
    AccessDeniedError,
    RoomNotFoundError,
    UserNotFoundError,
    RoomUserNotFoundError,
    RoomUserAlreadyExistsError,
)


def get_rooms_users_services(session: Session) -> list[RoomUser]:
    return get_rooms_users(session)


def create_room_user_service(
    room_id: int, user_id: int, my_user_id: int, session: Session
) -> RoomUser:

    if get_room_by_id(room_id, session) is None:
        raise RoomNotFoundError(room_id)

    if get_user_by_id(user_id, session) is None:
        raise UserNotFoundError(user_id)

    if is_user_in_room(room_id, user_id, session):
        raise RoomUserAlreadyExistsError(room_id, user_id)

    room_user = create_room_user(room_id, user_id, session)
    return save_room_user(room_user, session)


def delete_room_user_service(
    room_id: int, user_id: int, my_user_id: int, session: Session
) -> str:

    if get_user_by_id(user_id, session) is None:
        raise UserNotFoundError(user_id)

    if get_room_by_id(room_id, session) is None:
        raise RoomNotFoundError(room_id)

    if not is_user_in_room(room_id, my_user_id, session):
        raise AccessDeniedError()

    if not is_user_in_room(room_id, user_id, session):
        raise RoomUserNotFoundError(room_id, user_id)

    if user_id == my_user_id:
        raise AccessDeniedError()

    if count_users_in_room(room_id, session) <= 1:
        raise AccessDeniedError()

    delete_user_from_room(room_id, user_id, session)
    session.commit()
    return f"Из комнаты с ID {room_id} удалён пользователь с ID {user_id}"


def delete_users_from_room_service(room_id: int, session: Session) -> None:
    delete_users_from_room(room_id, session)


def save_room_user(room_user: RoomUser, session: Session) -> RoomUser:
    session.add(room_user)
    session.commit()
    session.refresh(room_user)
    return room_user
