
import os
from datetime import UTC, datetime, timedelta
from enum import Enum
from functools import wraps
from http import HTTPStatus

import jwt
from fastapi import HTTPException, Request

from to_do_api.models import User

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class TokenType(Enum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


def create_access_token(user: User) -> str:

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user.id),
        "type": TokenType.ACCESS.value,
        "exp": expire
    }
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user: User) -> str:
    
    expire = datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user.id),
        "type": TokenType.REFRESH.value,
        "exp": expire
    }
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def require_same_user():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request: Request | None = kwargs.get("request")

            user_path = request.path_params.get("user_id")
            user_jwt = request.state.user

            if user_jwt != user_path:
                raise HTTPException(
                    status_code=HTTPStatus.UNAUTHORIZED,
                    detail="user id doesn't match with token"
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
