from sqlmodel import SQLModel
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal


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


class MessagePage(SQLModel):
    items: list[MessageRead]
    total: int


class PaginationParams(BaseModel):
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)


class SortParams(SQLModel):
    order: Literal["asc", "desc"] = "desc"
