from fastapi import APIRouter, Depends

from src.models import RoomUser
from src.schemas import RoomUserRead, RoomUserCreate
from src.db import get_session
from src.services.room_user import (
    create_room_user_service,
    get_rooms_users_services,
    delete_room_user_service,
)

router = APIRouter(prefix="/room-user", tags=["room-user"])


@router.put("", response_model=RoomUserRead)
def create_room_user_endpoint(
    room_user: RoomUserCreate, session=Depends(get_session)
) -> RoomUser:
    return create_room_user_service(room_user, session)


@router.get("", response_model=list[RoomUserRead])
def get_rooms_users_endpoint(session=Depends(get_session)):
    return get_rooms_users_services(session)


@router.delete("/{room_id}/{user_id}", response_model=str)
def delete_room_user_endpoint(room_id: int, user_id: int, session=Depends(get_session)):
    return delete_room_user_service(room_id, user_id, session=session)
