from fastapi import APIRouter, Depends

from src.models import Room
from src.schemas import RoomCreate, RoomRead, UserRead
from src.services.rooms import (
    get_rooms_services,
    create_room_services,
    get_users_by_room_service,
)
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
