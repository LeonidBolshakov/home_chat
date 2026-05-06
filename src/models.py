from sqlmodel import SQLModel, Field, Index
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    hashed_password: str
    token_version: int = Field(default=0)


class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    room_id: int = Field(foreign_key="room.id", index=True)
    author_id: int = Field(foreign_key="user.id")

    text: str | None = None
    created_at: datetime


class RoomUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    room_id: int = Field(foreign_key="room.id")
    user_id: int = Field(foreign_key="user.id")

    __table_args__ = (Index("idx_room_user_room_id_user_id", "room_id", "user_id"),)
