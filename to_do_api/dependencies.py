import uuid
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from to_do_api.handlers.utils import ALGORITHM, SECRET_KEY

bearer_scheme = HTTPBearer()


def unauthorized(detail: str) -> JSONResponse:
    return HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_token_payload(credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],):
    try:
        return jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "type", "sub"]},
        )
    except jwt.ExpiredSignatureError:
        raise unauthorized("Expired token")
    except jwt.InvalidTokenError:
        raise unauthorized("Invalid token")


def get_current_user_id(
    payload: Annotated[dict, Depends(get_token_payload)],
) -> uuid.UUID:
    return payload["sub"]  # ou buscar o usuário no banco aqui


def require_same_user(
    user_id: str,  # from path: /users/{user_id}
    current_user_id: Annotated[str, Depends(get_current_user_id)],
) -> str:
    if user_id != current_user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="You can only access your own resource",
        )
    return current_user_id