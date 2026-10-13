import logging
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from to_do_api.dependencies import get_current_user_id, require_same_user
from to_do_api.exceptions import NotFoundError
from to_do_api.handlers.base import audit_logger
from to_do_api.handlers.utils import create_access_token, create_refresh_token
from to_do_api.models import Task, TaskManage, User, UserManage
from to_do_api.service.task import TaskService
from to_do_api.service.user import UserService

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

user_routes = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(get_current_user_id)])

user_service = UserService()
task_service = TaskService()

@user_routes.get("/")
@audit_logger.log_inbound(include_request_in_response=False)
def get_users(request: Request) -> list[User]:
    response = user_service.list()

    return response


@user_routes.post("/")
@audit_logger.log_inbound(include_request_in_response=False)
def create_users(request: Request, user_create: UserManage):
    user = User.from_create(user_create=user_create)
    response = user_service.insert(user=user)

    return response


@user_routes.get("/{user_id}", dependencies=[Depends(require_same_user)])
@audit_logger.log_inbound(include_request_in_response=False)
def get_user(request: Request, user_id: uuid.UUID) -> User:
    user = user_service.get(id=user_id)

    if not user:
        raise NotFoundError(id=user_id)

    return user

@user_routes.put("/{user_id}", dependencies=[Depends(require_same_user)])
@audit_logger.log_inbound(include_request_in_response=False)
def update_user(request: Request, user_id: uuid.UUID, user_manage: UserManage) -> User:
    user = user_service.get(id=user_id)

    if not user:
        raise NotFoundError(id=user_id)

    user.username = user_manage.username
    user.name = user_manage.name
    user.password = user_manage.password

    response = user_service.update(user=user)

    return response


@user_routes.get("/{user_id}/tasks", dependencies=[Depends(require_same_user)])
@audit_logger.log_inbound(include_request_in_response=False)
def get_tasks(request: Request, user_id: uuid.UUID) -> list[Task]:
    response = task_service.list(user_id)

    return response


@user_routes.post("/{user_id}/tasks", dependencies=[Depends(require_same_user)])
@audit_logger.log_inbound(include_request_in_response=False)
def create_tasks(request: Request, user_id: uuid.UUID, task_create: TaskManage) -> Task:
    user = user_service.get(id=user_id)

    if not user:
        raise NotFoundError(id=user_id)
    
    task = Task.from_create(user_id=user_id, task_create=task_create, user=user)
    response = task_service.insert(task=task)

    return response


@user_routes.get("/{user_id}/refresh_token", dependencies=[Depends(require_same_user)])
@audit_logger.log_inbound(include_request_in_response=False)
def refresh_token(request: Request):
    user = User(id=request.state.user, name="", username="")
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
