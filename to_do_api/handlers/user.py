import uuid
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request

from to_do_api.handlers.base import audit_logger
from to_do_api.models import Task, TaskCreate, User, UserCreate
from to_do_api.service.task import TaskService
from to_do_api.service.user import UserService

user_routes = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()
task_service = TaskService()

@user_routes.get("/")
@audit_logger.log_inbound(include_request_in_response=False)
async def get_users(request: Request) -> list[User]:
    try:
        response = user_service.list()

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )


@user_routes.post("/")
@audit_logger.log_inbound(include_request_in_response=False)
async def create_users(request: Request, user_create: UserCreate) -> User:
    try:
        user = User.from_create(user_create=user_create)
        response = user_service.insert(user=user)

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )

@user_routes.get("/{user_id}/tasks")
@audit_logger.log_inbound(include_request_in_response=False)
async def get_tasks(request: Request, user_id: uuid.UUID) -> list[Task]:
    try:
        response = task_service.list(user_id)

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )

@user_routes.post("/users/{user_id}/tasks")
@audit_logger.log_inbound(include_request_in_response=False)
async def create_tasks(request: Request, user_id: uuid.UUID, task_create: TaskCreate) -> Task:
    try:
        task = Task.from_create(user_id=user_id, task_create=task_create)
        response = task_service.insert(task=task)

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )
