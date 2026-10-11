from http import HTTPStatus

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from to_do_api.audit_logging.http_audit_logger import HTTPAuditLogger
from to_do_api.handlers.utils import create_access_token, create_refresh_token
from to_do_api.models import User, UserCreate
from to_do_api.service.user import UserService

base_routes = APIRouter()

user_service = UserService()

audit_logger = HTTPAuditLogger.from_env()
audit_logger.start()

@base_routes.post("/token")
def generate_token(request: Request, user_create: UserCreate):
    user = User.from_create(user_create=user_create)
    response = user_service.insert(user=user)

    # create access and refresh tokens
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "user": response.model_dump(mode='json'),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )
