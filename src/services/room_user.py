from sqlmodel import Session

from src.models import RoomUser
from src.schemas import RoomUserCreate
from src.crud.room_user import (
    create_room_user,
    get_rooms_users,
    get_room_user_by_room_id_and_user_id,
    delete_room_user,
)
from src.crud.rooms import get_room_by_id
from src.crud.users import get_user_by_id
from src.errors import (
    RoomUserAlreadyExistsError,
    RoomNotFoundError,
    UserNotFoundError,
    RoomUserNotFoundError,
    RoomUserNotDeletedError,
)


def get_rooms_users_services(session: Session) -> list[RoomUser]:
    return get_rooms_users(session)


def create_room_user_service(
    room_user_in: RoomUserCreate, session: Session
) -> RoomUser:
    if get_room_by_id(room_user_in.room_id, session) is None:
        raise RoomNotFoundError(room_user_in.room_id)

    if get_user_by_id(room_user_in.user_id, session) is None:
        raise UserNotFoundError(room_user_in.user_id)

    if get_room_user_by_room_id_and_user_id(
        room_user_in.room_id, room_user_in.user_id, session
    ):
        raise RoomUserAlreadyExistsError(room_user_in.room_id, room_user_in.user_id)

    room_user = create_room_user(room_user_in.room_id, room_user_in.user_id, session)
    return save_room_user(room_user, session)


def delete_room_user_service(room_id: int, user_id: int, session: Session) -> str:
    if get_user_by_id(user_id, session) is None:
        raise UserNotFoundError(user_id)

    if get_room_by_id(room_id, session) is None:
        raise RoomNotFoundError(room_id)

    if get_room_user_by_room_id_and_user_id(room_id, user_id, session) is None:
        raise RoomUserNotFoundError(room_id, user_id)

    delete_room_user(room_id, user_id, session)
    if get_room_user_by_room_id_and_user_id(room_id, user_id, session) is not None:
        raise RoomUserNotDeletedError(room_id, user_id)

    session.commit()
    return f"Из комнаты с ID {room_id} удалён пользователь с ID {user_id}"


def save_room_user(room_user: RoomUser, session: Session) -> RoomUser:
    session.add(room_user)
    session.commit()
    session.refresh(room_user)
    return room_user
