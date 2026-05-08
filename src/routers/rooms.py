from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.models import Room
from src.schemas import (
    RoomCreate,
    RoomRead,
    UserRead,
    PaginationParams,
    SortParams,
    MessagePage,
    RoomUpdate,
)
from src.services.rooms import (
    get_rooms_services,
    create_room_services,
    get_users_by_room_service,
    delete_room_service,
    get_room_service,
    update_room_service,
)
from src.services.messages import get_messages_page_by_room_for_user_service
from src.db import get_session
from src.auth import get_current_user_id

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomRead])
def get_rooms_endpoint(
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> list[Room]:
    return get_rooms_services(user_id, session)


@router.post("", response_model=RoomRead)
def create_room_endpoint(
    room: RoomCreate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Room:
    return create_room_services(room, session)


@router.get("/{room_id}/users", response_model=list[UserRead])
def get_users_by_room_endpoint(
    room_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    return get_users_by_room_service(room_id, user_id, session)


@router.get("/{room_id}/messages", response_model=MessagePage)
def get_messages_page_by_room_endpoint(
    room_id: int,
    user_id: int = Depends(get_current_user_id),
    pagination: PaginationParams = Depends(),
    sort_params: SortParams = Depends(),
    session: Session = Depends(get_session),
):
    return get_messages_page_by_room_for_user_service(
        room_id,
        user_id,
        pagination.limit,
        pagination.offset,
        sort_params.order,
        session,
    )


@router.delete("/{room_id}", response_model=str)
def delete_room_endpoint(
    room_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    return delete_room_service(room_id, user_id, session=session)


@router.get("/{room_id}", response_model=RoomRead)
def get_room_endpoint(
    room_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Room:
    return get_room_service(room_id, user_id, session=session)


@router.patch("/{room_id}", response_model=RoomRead)
def update_room_endpoint(
    room_id: int,
    room_in: RoomUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    return update_room_service(room_id, room_in, user_id, session=session)
