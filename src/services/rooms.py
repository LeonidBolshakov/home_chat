from sqlmodel import Session

from src.errors import RoomNotFoundError
from src.models import Room, User
from src.crud.rooms import get_rooms, create_room, get_users_by_room, get_room_by_id
from src.schemas import RoomCreate


def get_rooms_services(session: Session) -> list[Room]:
    return get_rooms(session)


def create_room_services(room_in: RoomCreate, session: Session) -> Room:
    room = create_room(room_in.title, session)
    return save_room(room, session)


def get_users_by_room_service(room_id: int, session: Session) -> list[User]:
    if get_room_by_id(room_id, session) is None:
        raise RoomNotFoundError(room_id)

    return get_users_by_room(room_id, session)


def save_room(room: Room, session: Session) -> Room:
    session.add(room)
    session.commit()
    session.refresh(room)
    return room
