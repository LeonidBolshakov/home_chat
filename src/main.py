from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.db import lifespan
from src.routers.users import router as users_router
from src.routers.rooms import router as rooms_router
from src.errors import UserAlreadyExistsError

app = FastAPI(lifespan=lifespan)


@app.exception_handler(UserAlreadyExistsError)
def user_already_exists_exception_handler(
    request: Request, exc: UserAlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


app.include_router(users_router)
app.include_router(rooms_router)
