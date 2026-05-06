from sqlmodel import Session, select, delete, func
from datetime import datetime, timezone
from typing import Callable

from src.models import Message


def create_message(
    room_id: int,
    author_id: int,
    text: str | None,
    session: Session,
) -> Message:
    return Message(
        room_id=room_id,
        author_id=author_id,
        text=text,
        created_at=datetime.now(timezone.utc),
    )


def get_messages_page_by_room(
    room_id: int,
    limit: int,
    offset: int,
    order: Callable,
    session: Session,
) -> list[Message]:

    statement = (
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(order(Message.created_at))
        .offset(offset)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def get_messages_page_with_total(
    room_id: int,
    limit: int,
    offset: int,
    order: Callable,
    session: Session,
) -> tuple[list[Message], int]:

    total_column = func.count().over().label("total")

    statement = (
        select(Message, total_column)
        .where(Message.room_id == room_id)
        .order_by(order(Message.created_at))
        .offset(offset)
        .limit(limit)
    )
    result = session.exec(statement).all()
    if not result:
        return [], 0

    messages = [row[0] for row in result]
    total_count = result[0][1]
    return messages, total_count


def get_messages(session: Session) -> list[Message]:
    statement = select(Message)
    return list(session.exec(statement).all())


def get_message_by_id(message_id: int, session: Session) -> Message | None:
    statement = select(Message).where(Message.id == message_id)
    return session.exec(statement).first()


def delete_messages_by_room(room_id: int, session: Session) -> None:
    statement = delete(Message).where(Message.room_id == room_id)  # type: ignore[arg-type]
    session.exec(statement)


def count_messages_by_room(room_id: int, session: Session) -> int:
    statement = select(func.count()).where(Message.room_id == room_id)
    return session.exec(statement).one()


def get_messages_page_by_user_id_with_total(
    user_id: int, limit: int, offset: int, order: Callable, session: Session
) -> tuple[list[Message], int]:
    total_column = func.count().over().label("total")
    statement = (
        select(Message, total_column)
        .where(Message.author_id == user_id)
        .order_by(order(Message.created_at))
        .limit(limit)
        .offset(offset)
    )
    result = session.exec(statement).all()
    if not result:
        return [], 0

    messages = [row[0] for row in result]
    total_count = result[0][1]
    return messages, total_count
