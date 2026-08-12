import logging
import uuid
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request

from to_do_api.audit_logging import HTTPAuditLogger
from to_do_api.models import Task, User
from to_do_api.service.task import TaskService
from to_do_api.service.user import UserService

__LOG_FMT = "{\"time\": \"%(asctime)s\", \"name\": \"[%(name)s]\", \"filename\": \"[%(filename)s]\", \"lineno\": \"[%(lineno)s]\", \"levelname\": \"%(levelname)s\", \"message\": \"%(message)s\"}"

app = FastAPI()

audit_logger = HTTPAuditLogger.from_env()
audit_logger.start()


logging.basicConfig(level=logging.INFO, format=__LOG_FMT)
root_logger = logging.getLogger()


@app.get("/users")
@audit_logger.log_inbound(include_request_in_response=False)
async def get_users(request: Request) -> list[User]:
    try:
        user_service = UserService()
        response = user_service.list()

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )


@app.post("/users")
@audit_logger.log_inbound(include_request_in_response=False)
async def create_users(request: Request, user: User) -> User:
    try:
        user_service = UserService()
        response = user_service.insert(user)

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )

@app.get("/users/{user_id}/tasks")
@audit_logger.log_inbound(include_request_in_response=False)
async def get_tasks(request: Request, user_id: uuid.UUID) -> list[Task]:
    try:
        task_service = TaskService()
        response = task_service.list(user=User(id=user_id, name="", username=""))

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )

@app.post("/users/{user_id}/tasks")
@audit_logger.log_inbound(include_request_in_response=False)
async def create_tasks(request: Request, user_id: uuid.UUID, task: Task) -> Task:
    try:
        task_service = TaskService()

        task.user = User(id=user_id, name="", username="")
        response = task_service.insert(task)

        return response
    except Exception as ex:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=ex,
        )