from sqlmodel import Session, select, delete, func

from src.models import RoomUser


def create_room_user(room_id: int, user_id: int, session: Session) -> RoomUser:
    return RoomUser(room_id=room_id, user_id=user_id)


def is_user_in_room(room_id: int, user_id: int, session: Session) -> bool:
    statement = select(RoomUser).where(
        (RoomUser.room_id == room_id) & (RoomUser.user_id == user_id)  # type: ignore[arg-type]
    )
    return session.exec(statement).first() is not None


def get_rooms_users(session: Session) -> list[RoomUser]:
    statement = select(RoomUser)
    return list(session.exec(statement).all())


def delete_users_from_room(room_id: int, session: Session) -> None:
    statement = delete(RoomUser).where(
        RoomUser.room_id == room_id  # type: ignore[arg-type]
    )
    session.exec(statement)


def delete_user_from_room(room_id: int, user_id: int, session: Session) -> None:
    statement = delete(RoomUser).where(
        (RoomUser.room_id == room_id) & (RoomUser.user_id == user_id)  # type: ignore[arg-type]
    )
    session.exec(statement)


def count_users_in_room(room_id: int, session: Session) -> int:
    statement = (
        select(func.count()).select_from(RoomUser).where(RoomUser.room_id == room_id)
    )
    return session.exec(statement).one()
