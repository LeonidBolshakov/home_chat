from typing import Callable
from sqlmodel import Session, asc, desc

from src.errors import AccessDeniedError
from src.models import Message
from src.schemas import MessageCreate, MessagePage
from src.crud.room_user import is_user_in_room
from src.crud.messages import (
    create_message,
    get_messages,
    get_message_by_id,
    delete_messages_by_room,
    get_messages_page_with_total,
    get_messages_page_by_user_id_with_total,
)


def create_message_service(
    message_in: MessageCreate,
    user_id: int,
    session: Session,
) -> Message:

    if not is_user_in_room(message_in.room_id, user_id, session):
        raise AccessDeniedError()

    message = create_message(message_in.room_id, user_id, message_in.text, session)
    return save_message(message, session)


def save_message(message: Message, session: Session):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message


def get_messages_service(user_id: int, session: Session) -> list[Message]:
    return get_messages(user_id, session)


def get_messages_page_by_room_for_user_service(
    room_id: int,
    user_id: int,
    limit: int,
    offset: int,
    sorting_direction: str,
    session: Session,
) -> MessagePage:
    if not is_user_in_room(room_id, user_id, session):
        raise AccessDeniedError()
    order = get_sorting_direction(sorting_direction)

    items, total = get_messages_page_with_total(
        room_id,
        limit,
        offset,
        order,
        session,
    )

    return MessagePage(
        items=items,
        total=total,
    )


def delete_messages_by_room_service(room_id: int, session: Session) -> None:
    delete_messages_by_room(room_id, session)


def delete_message_service(message_id: int, user_id: int, session: Session) -> None:
    message = get_message_by_id(message_id, session)

    if message is None:
        raise AccessDeniedError()

    if message.author_id != user_id:
        raise AccessDeniedError()

    session.delete(message)
    session.commit()


def update_message_service(
    message_id: int, user_id: int, new_text_message: str, session: Session
) -> Message:
    message = get_message_by_id(message_id, session)

    if message is None:
        raise AccessDeniedError()

    if message.author_id != user_id:
        raise AccessDeniedError()
    if not new_text_message.strip():
        raise ValueError("текст сообщения не может быть пустым")

    message.text = new_text_message
    session.commit()
    session.refresh(message)
    return message


def get_me_messages_service(
    user_id: int, limit: int, offset: int, sorting_direction: str, session: Session
) -> MessagePage:
    order = get_sorting_direction(sorting_direction)
    items, total = get_messages_page_by_user_id_with_total(
        user_id, limit, offset, order, session
    )
    return MessagePage(items=items, total=total)


def get_sorting_direction(sorting_direction: str) -> Callable:
    match sorting_direction:
        case "asc":
            order = asc
        case "desc":
            order = desc
        case _:
            raise ValueError(f"Неизвестный порядок сортировки: {sorting_direction}")

    return order
