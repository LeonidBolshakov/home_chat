from sqlmodel import Session

from src.errors import RoomNotFoundError, AccessDeniedError
from src.models import Room, User
from src.schemas import RoomCreate, RoomUpdate
from src.crud.rooms import (
    get_rooms,
    create_room,
    get_users_by_room,
    get_room_by_id,
    delete_room,
)
from src.services.room_user import delete_users_from_room_service
from src.services.messages import delete_messages_by_room_service, is_user_in_room


def get_rooms_services(user_id: int, session: Session) -> list[Room]:
    return get_rooms(user_id, session)


def create_room_services(room_in: RoomCreate, session: Session) -> Room:
    room = create_room(room_in.title, session)
    return save_room(room, session)


def get_users_by_room_service(
    room_id: int, user_id: int, session: Session
) -> list[User]:

    if not is_user_in_room(room_id, user_id, session):
        raise AccessDeniedError()

    return get_users_by_room(room_id, session)


def delete_room_service(room_id: int, user_id: int, session: Session) -> str:
    if get_room_by_id(room_id, session) is None:
        raise RoomNotFoundError(room_id)

    if not is_user_in_room(room_id, user_id, session):
        raise AccessDeniedError()

    delete_users_from_room_service(room_id, session)
    delete_messages_by_room_service(room_id, session)
    delete_room(room_id, session)

    session.commit()
    return f"Комната с ID {room_id} удалена"


def get_room_service(room_id: int, user_id: int, session: Session) -> Room:
    if not is_user_in_room(room_id, user_id, session):
        raise AccessDeniedError()

    room = get_room_by_id(room_id, session)
    if room is None:
        raise RoomNotFoundError(room_id)

    return room


def update_room_service(
    room_id: int, room_in: RoomUpdate, user_id: int, session: Session
) -> Room:
    if not is_user_in_room(room_id, user_id, session):
        raise AccessDeniedError()

    room = get_room_by_id(room_id, session)
    if room is None:
        raise RoomNotFoundError(room_id)

    room.title = room_in.title
    session.commit()
    session.refresh(room)

    return room


def save_room(room: Room, session: Session) -> Room:
    session.add(room)
    session.commit()
    session.refresh(room)
    return room
