from sqlmodel import Session

from src.models import Room
from src.crud.rooms import get_rooms, create_room
from src.schemas import RoomCreate


def get_rooms_services(session: Session) -> list[Room]:
    return get_rooms(session)


def create_room_services(room_in: RoomCreate, session: Session) -> Room:
    room = create_room(room_in.title, session)
    return save_room(room, session)


def save_room(room: Room, session: Session) -> Room:
    session.add(room)
    session.commit()
    session.refresh(room)
    return room
