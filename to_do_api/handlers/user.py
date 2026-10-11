import logging
import uuid
from http import HTTPStatus

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from to_do_api.handlers.base import audit_logger
from to_do_api.handlers.utils import create_access_token, create_refresh_token
from to_do_api.models import Task, TaskCreate, User, UserCreate
from to_do_api.service.task import TaskService
from to_do_api.service.user import UserService

logger = logging.getLogger(__name__)

user_routes = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()
task_service = TaskService()

@user_routes.get("/")
@audit_logger.log_inbound(include_request_in_response=False)
def get_users(request: Request) -> list[User]:
    response = user_service.list()

    return response


@user_routes.post("/")
@audit_logger.log_inbound(include_request_in_response=False)
def create_users(request: Request, user_create: UserCreate):
    user = User.from_create(user_create=user_create)
    response = user_service.insert(user=user)

    return response


@user_routes.get("/{user_id}/tasks")
@audit_logger.log_inbound(include_request_in_response=False)
def get_tasks(request: Request, user_id: uuid.UUID) -> list[Task]:
    response = task_service.list(user_id)

    return response


@user_routes.post("/{user_id}/tasks")
@audit_logger.log_inbound(include_request_in_response=False)
def create_tasks(request: Request, user_id: uuid.UUID, task_create: TaskCreate) -> Task:
    task = Task.from_create(user_id=user_id, task_create=task_create)
    response = task_service.insert(task=task)

    return response


@user_routes.get("/{user_id}/refresh_token")
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
