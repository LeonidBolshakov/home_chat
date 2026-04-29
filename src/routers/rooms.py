from fastapi import APIRouter, Depends

from src.models import Room
from src.schemas import (
    RoomCreate,
    RoomRead,
    UserRead,
    PaginationParams,
    SortParams,
    MessagePage,
)
from src.services.rooms import (
    get_rooms_services,
    create_room_services,
    get_users_by_room_service,
    delete_room_service,
)
from src.services.messages import get_messages_page_by_room_for_user_service
from src.db import get_session

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomRead])
def get_rooms_endpoint(session=Depends(get_session)) -> list[Room]:
    return get_rooms_services(session)


@router.post("", response_model=RoomRead)
def create_room_endpoint(room: RoomCreate, session=Depends(get_session)) -> Room:
    return create_room_services(room, session)


@router.get("/{room_id}/users", response_model=list[UserRead])
def get_users_by_room_endpoint(room_id: int, session=Depends(get_session)):
    return get_users_by_room_service(room_id, session)


@router.delete("/{room_id}", response_model=str)
def delete_room_endpoint(room_id: int, session=Depends(get_session)):
    return delete_room_service(room_id, session=session)


@router.get("/{room_id}/messages", response_model=MessagePage)
def get_messages_page_by_room_endpoint(
    room_id: int,
    user_id: int,
    pagination: PaginationParams = Depends(),
    sort_params: SortParams = Depends(),
    session=Depends(get_session),
):
    return get_messages_page_by_room_for_user_service(
        room_id,
        user_id,
        pagination.limit,
        pagination.offset,
        sort_params.order,
        session,
    )
