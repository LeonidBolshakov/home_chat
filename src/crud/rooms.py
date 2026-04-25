from sqlmodel import select, Session
from src.models import Room


def get_room_by_id(room_id: int, session: Session) -> Room | None:
    statemant = select(Room).where(Room.id == room_id)
    return session.exec(statemant).first()


def get_room_by_name(title: str, session: Session) -> Room | None:
    statemant = select(Room).where(Room.title == title)
    return session.exec(statemant).first()


def create_room(title: str, session: Session) -> Room:
    return Room(title=title)


def get_rooms(session: Session) -> list[Room]:
    statemant = select(Room)
    return list(session.exec(statemant).all())
