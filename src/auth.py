from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.db import get_session
from src.crud.users import get_user_by_id

SECRET_KEY = "dev-secret-key"
ALGORITHM = "HS256"

security = HTTPBearer()


def create_access_token(user_id: int, token_version: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=1)

    payload = {
        "sub": str(user_id),
        "token_version": token_version,
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> int:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
        token_version = int(payload["token_version"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Неверный токен")

    user = get_user_by_id(user_id, session)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    if token_version != user.token_version:
        raise HTTPException(status_code=401, detail="Неверная версия токена")

    return user_id


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
