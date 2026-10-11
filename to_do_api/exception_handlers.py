
import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from to_do_api.exceptions import UserAlreadyExistsError

logger = logging.getLogger(__name__)


def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    logger.error(f"User already exists: username {exc.username}")

    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        content={"detail": f"O username '{exc.username}' já está em uso."},
    )


def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserAlreadyExistsError, user_exists_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
