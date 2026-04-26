from sqlmodel import Session, select
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


def get_messages_by_room(room_id: int, session: Session) -> list[Message]:
    statement = select(Message).where(Message.room_id == room_id)
    return sorted(
        list(session.exec(statement).all()), key=lambda m: m.created_at, reverse=True
    )


def get_messages(session: Session) -> list[Message]:
    statement = select(Message)
    return list(session.exec(statement).all())
