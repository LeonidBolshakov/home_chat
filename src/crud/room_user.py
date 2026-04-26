from sqlmodel import Session, select, delete

from src.models import RoomUser


def create_room_user(room_id: int, user_id: int, session: Session) -> RoomUser:
    return RoomUser(room_id=room_id, user_id=user_id)


def get_room_user_by_room_id_and_user_id(
    room_id: int, user_id: int, session: Session
) -> RoomUser | None:
    statement = select(RoomUser).where(
        (RoomUser.room_id == room_id) & (RoomUser.user_id == user_id)  # type: ignore[arg-type]
    )
    return session.exec(statement).first()


def get_rooms_users(session: Session) -> list[RoomUser]:
    statement = select(RoomUser)
    return list(session.exec(statement).all())


def delete_room_user(room_id: int, user_id: int, session: Session) -> None:
    statement = delete(RoomUser).where(
        (RoomUser.room_id == room_id) & (RoomUser.user_id == user_id)  # type: ignore[arg-type]
    )
    session.exec(statement)
