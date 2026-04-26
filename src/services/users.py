from sqlmodel import Session

from src.schemas import UserCreate
from src.models import User, Room
from src.errors import UserAlreadyExistsError, UserNotFoundError
from src.crud.users import (
    get_users,
    create_user,
    get_user_by_name,
    get_rooms_by_user,
    get_user_by_id,
)


def get_users_service(session: Session) -> list[User]:
    return get_users(session)


def create_user_service(user_in: UserCreate, session: Session) -> User:
    user_by_name = get_user_by_name(user_in.name, session)
    if user_by_name is not None:
        raise UserAlreadyExistsError(user_in.name)
    user = create_user(user_in.name, session)
    return save_user(user, session)


def get_rooms_by_user_service(user_id: int, session: Session) -> list[Room]:
    if get_user_by_id(user_id, session) is None:
        raise UserNotFoundError(user_id)

    return get_rooms_by_user(user_id, session)


def save_user(user: User, session: Session) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
