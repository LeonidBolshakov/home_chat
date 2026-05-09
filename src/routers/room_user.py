from fastapi import APIRouter, Depends

from src.models import RoomUser
from src.schemas import RoomUserRead
from src.db import get_session
from src.auth import get_current_user_id
from src.services.room_user import (
    create_room_user_service,
    get_rooms_users_services,
    delete_room_user_service,
)

router = APIRouter(prefix="/room_user", tags=["room_user"])


@router.put("/{room_id}/users/{user_id}", response_model=RoomUserRead)
def create_room_user_endpoint(
    room_id: int,
    user_id: int,
    my_user_id: int = Depends(get_current_user_id),
    session=Depends(get_session),
) -> RoomUser:
    return create_room_user_service(room_id, user_id, my_user_id, session)


@router.get("", response_model=list[RoomUserRead])
def get_rooms_users_endpoint(
    user_id: int = Depends(get_current_user_id), session=Depends(get_session)
):
    return get_rooms_users_services(session)


@router.delete("/{room_id}/users/{user_id}", response_model=str)
def delete_room_user_endpoint(
    room_id: int,
    user_id: int,
    my_user_id: int = Depends(get_current_user_id),
    session=Depends(get_session),
):
    return delete_room_user_service(room_id, user_id, my_user_id, session=session)
