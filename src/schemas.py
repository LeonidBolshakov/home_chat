from sqlmodel import SQLModel
from datetime import datetime


class UserCreate(SQLModel):
    name: str


class UserRead(SQLModel):
    id: int
    name: str


class RoomCreate(SQLModel):
    title: str


class RoomRead(SQLModel):
    id: int
    title: str


class MessageCreate(SQLModel):
    room_id: int
    author_id: int

    text: str | None = None


class MessageRead(SQLModel):
    id: int

    room_id: int
    author_id: int

    text: str | None = None
    created_at: datetime


class RoomUserCreate(SQLModel):
    room_id: int
    user_id: int


class RoomUserRead(SQLModel):
    id: int

    room_id: int
    user_id: int
