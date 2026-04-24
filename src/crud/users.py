from sqlmodel import select, Session
from src.models import User


def get_users(session: Session) -> list[User]:
    statemant = select(User)
    return list(session.exec(statemant).all())


def get_user_by_name(name: str, session: Session) -> User | None:
    statemant = select(User).where(User.name == name)
    return session.exec(statemant).first()


def create_user(name: str, session: Session) -> User:
    return User(name=name)
