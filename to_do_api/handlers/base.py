from http import HTTPStatus

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from to_do_api.audit_logging.http_audit_logger import HTTPAuditLogger
from to_do_api.exceptions import LoginError
from to_do_api.handlers.utils import create_access_token, create_refresh_token
from to_do_api.models import Login, User, UserManage
from to_do_api.service.base import password_hash
from to_do_api.service.user import UserService

base_routes = APIRouter()

user_service = UserService()

audit_logger = HTTPAuditLogger.from_env()
audit_logger.start()

@base_routes.post("/token")
def generate_token(request: Request, user_create: UserManage):
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


@base_routes.post("/login")
def login(request: Request, login: Login):
    user = user_service.get_by_username(login.username)

    if not user:
        raise LoginError(username=login.username)

    # verify_and_update confere a senha e, se os parâmetros do hash
    # ficaram defasados, devolve um hash novo para atualizar no banco
    valid, updated_hash = password_hash.verify_and_update(
        login.password, user.password
    )
    if not valid:
        raise LoginError(username=login.username)
 

    # create access and refresh tokens
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={
            "user": user.model_dump(mode='json'),
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )

@base_routes.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
