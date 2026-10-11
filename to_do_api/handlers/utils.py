
import os
from datetime import UTC, datetime, timedelta
from enum import Enum

import jwt

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
