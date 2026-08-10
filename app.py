import logging
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request

from to_do_api.audit_logging import HTTPAuditLogger
from to_do_api.models import User
from to_do_api.service.user import UserService

__LOG_FMT = "{\"time\": \"%(asctime)s\", \"name\": \"[%(name)s]\", \"filename\": \"[%(filename)s]\", \"lineno\": \"[%(lineno)s]\", \"levelname\": \"%(levelname)s\", \"message\": \"%(message)s\"}"

app = FastAPI()
audit_logger = HTTPAuditLogger.from_env()
audit_logger.start()


logging.basicConfig(level=logging.INFO, format=__LOG_FMT)
root_logger = logging.getLogger()


@app.get("/users")
@audit_logger.log_inbound(include_request_in_response=False)
def get_users(request: Request) -> list[User]:
    try:
        user_service = UserService()
        response = user_service.list_users()

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )


@app.post("/users")
@audit_logger.log_inbound(include_request_in_response=False)
def create_users(request: Request, user: User) -> User:
    try:
        user_service = UserService()
        response = user_service.insert_user(user)

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )
