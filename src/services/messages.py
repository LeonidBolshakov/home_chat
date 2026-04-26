from sqlmodel import Session
from src.models import Message
from src.schemas import MessageCreate
from src.crud.users import get_user_by_id
from src.crud.rooms import get_room_by_id
from src.crud.messages import create_message, get_messages, get_messages_by_room

from src.errors import UserNotFoundError, RoomNotFoundError


def create_message_service(
    message_in: MessageCreate,
    session: Session,
) -> Message:

    if get_user_by_id(message_in.author_id, session) is None:
        raise UserNotFoundError(message_in.author_id)

    if get_room_by_id(message_in.room_id, session=session) is None:
        raise RoomNotFoundError(message_in.room_id)

    message = create_message(
        message_in.room_id, message_in.author_id, message_in.text, session
    )
    return save_message(message, session)


def save_message(message: Message, session: Session):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_messages_service(session: Session) -> list[Message]:
    return get_messages(session)


def get_messages_by_room_service(room_id: int, session: Session) -> list[Message]:
    if get_room_by_id(room_id, session) is None:
        raise RoomNotFoundError(room_id)
    return get_messages_by_room(room_id, session)
