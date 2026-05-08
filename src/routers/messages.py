from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.schemas import (
    MessageRead,
    MessageCreate,
    MessageUpdate,
)
from src.models import Message
from src.db import get_session
from src.auth import get_current_user_id
from src.services.messages import (
    get_messages_service,
    create_message_service,
    delete_message_service,
    update_message_service,
)

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("", response_model=list[MessageRead])
def get_messages_endpoint(
    user_id: int = Depends(get_current_user_id), session=Depends(get_session)
) -> list[Message]:
    return get_messages_service(user_id, session)


@router.post("", response_model=MessageRead)
def create_message_endpoint(
    message: MessageCreate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Message:
    return create_message_service(message, user_id, session)


@router.delete("/{message_id}")
def delete_message_endpoint(
    message_id: int,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> dict[str, str]:
    delete_message_service(message_id, user_id, session)
    return {"message": "сообщение удалено"}


@router.patch("/messages/{message_id}", response_model=MessageRead)
def update_message_endpoint(
    message_id: int,
    message_in: MessageUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
) -> Message:
    return update_message_service(message_id, user_id, message_in.text, session)
