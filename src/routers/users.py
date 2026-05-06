from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.schemas import (
    UserRead,
    UserCreate,
    TokenResponse,
    UserRegister,
    UserLogin,
    PaginationParams,
    SortParams,
    MessagePage,
)
from src.models import User
from src.db import get_session
from src.auth import get_current_user_id
from src.services.messages import get_me_messages_service
from src.services.users import (
    get_users_service,
    create_user_service,
    logout_service,
    login_service,
    register_service,
    get_me_service,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def get_users_endpoint(session=Depends(get_session)) -> list[User]:
    return get_users_service(session)


@router.post("", response_model=UserRead)
def create_user_endpoint(user: UserCreate, session=Depends(get_session)) -> User:
    return create_user_service(user, session)


@router.post("/login", response_model=TokenResponse)
def login(user_in: UserLogin, session: Session = Depends(get_session)):

    token = login_service(user_in.name, user_in.password, session)
    return TokenResponse(access_token=token)


@router.post("/logout")
def logout(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    logout_service(user_id, session)
    return {"message": "Logged out"}


@router.post("/register", response_model=UserRead)
def register_endpoint(user_in: UserRegister, session: Session = Depends(get_session)):
    return register_service(user_in.name, user_in.password, session)


@router.get("/me/messages", response_model=MessagePage)
def get_me_messages_endpoint(
    user_id: int = Depends(get_current_user_id),
    pagination_params: PaginationParams = Depends(PaginationParams),
    sort_params: SortParams = Depends(SortParams),
    session: Session = Depends(get_session),
) -> MessagePage:
    return get_me_messages_service(
        user_id,
        pagination_params.limit,
        pagination_params.offset,
        sort_params.order,
        session,
    )


@router.get("/me", response_model=UserRead)
def get_me_endpoint(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    return get_me_service(user_id, session)
