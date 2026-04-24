from sqlmodel import SQLModel


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
