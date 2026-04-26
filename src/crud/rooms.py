from sqlmodel import select, Session
from sqlalchemy import exists, and_

from src.models import Room, RoomUser, User


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


def get_users_by_room(room_id: int, session: Session) -> list[User]:
    statement = (
        select(User)
        .join(RoomUser, RoomUser.user_id == User.id)
        .where(RoomUser.room_id == room_id)
    )
    return list(session.exec(statement).all())
