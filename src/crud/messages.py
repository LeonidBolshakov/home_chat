from sqlmodel import Session, select, delete, desc, asc, func
from datetime import datetime, timezone

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


def get_messages_by_room(
    room_id: int, limit: int, offset: int, sorting_direction: str, session: Session
) -> list[Message]:
    match sorting_direction:
        case "asc":
            order = asc
        case "desc":
            order = desc
        case _:
            raise ValueError(f"Неизвестный порядок сортировки: {sorting_direction}")

    statement = (
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(order(Message.created_at))
        .offset(offset)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def get_messages(session: Session) -> list[Message]:
    statement = select(Message)
    return list(session.exec(statement).all())


def delete_messages_by_room(room_id: int, session: Session) -> None:
    statement = delete(Message).where(Message.room_id == room_id)  # type: ignore[arg-type]
    session.exec(statement)


def count_messages_by_room(room_id: int, session: Session) -> int:
    statement = select(func.count()).where(Message.room_id == room_id)
    return session.exec(statement).one()
