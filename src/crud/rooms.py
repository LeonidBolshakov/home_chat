from sqlmodel import select, Session
from src.models import Room


def get_room_by_id(room_id: int, session: Session) -> Room | None:
    statement = select(Room).where(Room.id == room_id)
    return session.exec(statement).first()


def get_room_by_name(title: str, session: Session) -> Room | None:
    statement = select(Room).where(Room.title == title)
    return session.exec(statement).first()


def create_room(title: str, session: Session) -> Room:
    return Room(title=title)


def get_rooms(session: Session) -> list[Room]:
    statement = select(Room)
    return list(session.exec(statement).all())
