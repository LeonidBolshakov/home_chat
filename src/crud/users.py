from sqlmodel import select, Session
from sqlalchemy import exists, and_
from src.models import User, Room, Message, RoomUser


def get_users(session: Session) -> list[User]:
    statement = select(User)
    return list(session.exec(statement).all())


def get_user_by_id(user_id: int, session: Session) -> User | None:
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()


def get_user_by_name(name: str, session: Session) -> User | None:
    statement = select(User).where(User.name == name)
    return session.exec(statement).first()


def create_user(name: str, session: Session) -> User:
    return User(name=name)


def get_rooms_by_user_old(user_id: int, session: Session) -> list[Room]:
    statement = select(Room).where(
        exists().where(
            and_(
                Message.author_id == user_id,  # type: ignore[arg-type]
                Room.id == Message.room_id,  # type: ignore[arg-type]
            )
        )
    )
    return list(session.exec(statement).all())


def get_rooms_by_user(user_id: int, session: Session) -> list[Room]:
    statement = select(Room).where(
        exists().where(
            and_(
                RoomUser.user_id == user_id,  # type: ignore[arg-type]
                Room.id == RoomUser.room_id,  # type: ignore[arg-type]
            )
        )
    )
    return list(session.exec(statement).all())
