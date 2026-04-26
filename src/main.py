from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.db import lifespan
from src.routers.users import router as users_router
from src.routers.rooms import router as rooms_router
from src.routers.messages import router as messages_router
from src.routers.room_user import router as room_user_router
from src.errors import (
    UserAlreadyExistsError,
    RoomUserAlreadyExistsError,
    UserNotFoundError,
    RoomNotFoundError,
    RoomUserNotDeletedError,
    RoomUserNotFoundError,
)

app = FastAPI(lifespan=lifespan)


@app.exception_handler(UserAlreadyExistsError)
def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(RoomUserAlreadyExistsError)
def room_user_already_exists_exception_handler(
    request: Request, exc: RoomUserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(UserNotFoundError)
def user_does_not_exist_exception_handler(
    request: Request, exc: UserNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(RoomNotFoundError)
def room_does_not_exist_exception_handler(
    request: Request, exc: RoomNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(RoomUserNotDeletedError)
def room_user_not_deleted_error(
    request: Request, exc: RoomUserNotDeletedError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(RoomUserNotFoundError)
def room_user_not_found_error(
    request: Request, exc: RoomUserNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(messages_router)
app.include_router(room_user_router)
