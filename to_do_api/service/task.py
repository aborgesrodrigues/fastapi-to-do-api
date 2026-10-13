import uuid

from to_do_api.dao.task import TaskDAO
from to_do_api.models import Task
from to_do_api.service.base import Service


class TaskService(Service):
    def __init__(self):
        self.__dao = TaskDAO()

    def insert(self, task: Task) -> Task:
        row_count = self.__dao.insert(task)

        if row_count != 1:
            raise Exception("Error inserting task")
        return task

    def list(self, user_id: uuid.UUID) -> list[Task]:
        return self.__dao.list(user_id)
