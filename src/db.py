from fastapi import FastAPI
from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager

DATABASE_URL = "sqlite:///C:/1_python_web/home_chat/db_home_chat.db"
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
