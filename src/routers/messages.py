from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.schemas import MessageRead, MessageCreate
from src.models import Message
from src.db import get_session
from src.services.messages import get_messages_service, create_message_service

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[Message])
def get_messages_endpoint(session=Depends(get_session)) -> list[Message]:
    return get_messages_service(session)


@router.post("", response_model=MessageRead)
def create_message_endpoint(
    room: MessageCreate, session: Session = Depends(get_session)
) -> Message:
    return create_message_service(room, session)
