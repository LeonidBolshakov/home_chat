from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.schemas import (
    MessageRead,
    MessageCreate,
    MessagePage,
    PaginationParams,
    SortParams,
)
from src.models import Message
from src.db import get_session
from src.services.messages import (
    get_messages_service,
    create_message_service,
    get_messages_by_room_service,
    get_messages_page_by_room_service,
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[MessageRead])
def get_messages_endpoint(session=Depends(get_session)) -> list[Message]:
    return get_messages_service(session)


@router.post("", response_model=MessageRead)
def create_message_endpoint(
    room: MessageCreate, session: Session = Depends(get_session)
) -> Message:
    return create_message_service(room, session)


@router.get("/{room_id}", response_model=list[MessageRead])
def get_messages_by_room_endpoint(
    room_id: int,
    pagination: PaginationParams = Depends(),
    sort: SortParams = Depends(SortParams),
    session: Session = Depends(get_session),
) -> list[Message]:
    return get_messages_by_room_service(
        room_id,
        pagination.limit,
        pagination.offset,
        sort.order,
        session,
    )


@router.get("/{room_id}/count", response_model=MessagePage)
def get_messages_by_room_total_endpoint(
    room_id: int,
    pagination: PaginationParams = Depends(),
    sort: SortParams = Depends(SortParams),
    session: Session = Depends(get_session),
) -> MessagePage:
    return get_messages_page_by_room_service(
        room_id,
        pagination.limit,
        pagination.offset,
        sort.order,
        session,
    )
