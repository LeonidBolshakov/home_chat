from fastapi import APIRouter, Depends

from src.models import Room
from src.schemas import RoomCreate, RoomRead
from src.services.rooms import get_rooms_services, create_room_services
from src.db import get_session

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomRead])
def get_rooms_endpoint(session=Depends(get_session)) -> list[Room]:
    return get_rooms_services(session)


@router.post("", response_model=RoomRead)
def create_room_endpoint(room: RoomCreate, session=Depends(get_session)) -> Room:
    return create_room_services(room, session)
