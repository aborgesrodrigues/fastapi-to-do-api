import uuid

from to_do_api.dao.task import TaskDAO
from to_do_api.models import Task
from to_do_api.service.base import Service


class TaskService(Service):
    def __init__(self):
        super().__init__()
        self.__dao = TaskDAO()

    def insert(self, task: Task) -> Task:
        self.__dao.insert(task)

        return task

    def get(self, id: uuid.UUID) -> Task:
        return self.__dao.get(id=id)

    def update(self, task: Task) -> Task:
        self.__dao.update(task)

        return task

    def delete(self, id: uuid.UUID) -> Task:
        return self.__dao.delete(id=id)

    def list(self, user_id: uuid.UUID) -> list[Task]:
        return self.__dao.list(user_id)
        