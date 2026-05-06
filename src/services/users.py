from sqlmodel import Session
from fastapi import HTTPException

from src.schemas import UserCreate
from src.models import User
from src.errors import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCredentialsError,
)
from src.auth import hash_password, create_access_token, verify_password
from src.crud.users import (
    get_users,
    create_user,
    get_user_by_name,
    get_user_by_id,
)


def get_users_service(session: Session) -> list[User]:
    return get_users(session)


def create_user_service(user_in: UserCreate, session: Session) -> User:
    user_by_name = get_user_by_name(user_in.name, session)

    if user_by_name is not None:
        raise UserAlreadyExistsError(user_in.name)

    hashed_password = hash_password(user_in.password)
    user = create_user(user_in.name, hashed_password, session)
    return save_user(user, session)


def login_service(username: str, password: str, session: Session) -> str:
    user = get_user_by_name(username, session)

    if user is None or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()

    if user.id is None:
        raise HTTPException(status_code=500, detail="User id is missing")

    return create_access_token(user.id, user.token_version)


def logout_service(user_id: int, session: Session) -> None:
    user = get_user_by_id(user_id, session)

    if user is None:
        raise UserNotFoundError(user_id)

    user.token_version += 1
    session.commit()


def register_service(username: str, password: str, session: Session) -> User:
    user = get_user_by_name(username, session)
    if user is not None:
        raise UserAlreadyExistsError(username)

    hashed_password = hash_password(password)
    user = create_user(username, hashed_password, session)
    return save_user(user, session)


def get_me_service(user_id: int, session: Session) -> User:
    user = get_user_by_id(user_id, session)
    if user is None:
        raise UserNotFoundError(user_id)
    return user


def save_user(user: User, session: Session) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
