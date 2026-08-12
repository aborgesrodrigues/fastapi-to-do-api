import uuid

from to_do_api.dao.task import TaskDAO
from to_do_api.models import Task, User


class TaskService:
    def __init__(self):
        self.__dao = TaskDAO()

    def insert(self, task: Task) -> Task:
        task.id = str(uuid.uuid4())
        row_count = self.__dao.insert(task)

        if row_count != 1:
            raise Exception("Error inserting task")
        return task

    def list(self, user: User) -> list[Task]:
        return self.__dao.list(user)
