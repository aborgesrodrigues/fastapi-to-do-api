import logging
import uuid

from fastapi import APIRouter, Request

from to_do_api.exceptions import NotFoundError
from to_do_api.handlers.base import audit_logger
from to_do_api.models import Task, TaskManage
from to_do_api.service.task import TaskService

logger = logging.getLogger(__name__)

task_routes = APIRouter(prefix="/tasks", tags=["tasks"])

task_service = TaskService()

@task_routes.get("/")
@audit_logger.log_inbound(include_request_in_response=False)
def get_tasks(request: Request) -> list[Task]:
    response = task_service.list()

    return response


@task_routes.get("/{task_id}")
@audit_logger.log_inbound(include_request_in_response=False)
def get_task(request: Request, task_id: uuid.UUID) -> Task:
    response = task_service.get(id=task_id)

    if not response:
        raise NotFoundError(id=task_id)

    return response


@task_routes.put("/{task_id}")
@audit_logger.log_inbound(include_request_in_response=False)
def update_task(request: Request, task_id: uuid.UUID, task_manage: TaskManage) -> Task:
    task = task_service.get(id=task_id)

    if not task:
        raise NotFoundError(id=task_id)

    task.description = task_manage.description
    task.state = task_manage.state

    response = task_service.update(task=task)

    return response


@task_routes.delete("/{task_id}")
@audit_logger.log_inbound(include_request_in_response=False)
def delete_task(request: Request, task_id: uuid.UUID):
    task = task_service.get(id=task_id)

    if not task:
        raise NotFoundError(id=task_id)

    task_service.de(task=task)
