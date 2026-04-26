from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str


class Room(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    room_id: int = Field(foreign_key="room.id")
    author_id: int = Field(foreign_key="user.id")

    text: str | None = None
    created_at: datetime


class RoomUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    room_id: int = Field(foreign_key="room.id")
    user_id: int = Field(foreign_key="user.id")
