from fastapi import APIRouter, Depends

from src.schemas import UserRead, UserCreate
from src.models import User
from src.db import get_session
from src.services.users import (
    get_users_service,
    create_user_service,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def get_users_endpoint(session=Depends(get_session)) -> list[User]:
    return get_users_service(session)


@router.post("", response_model=UserRead)
def create_user_endpoint(user: UserCreate, session=Depends(get_session)) -> User:
    return create_user_service(user, session)
