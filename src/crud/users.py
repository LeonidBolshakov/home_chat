from sqlmodel import select, Session
from src.models import User


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
