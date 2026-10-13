
import uuid

from to_do_api.dao.dao import DAO
from to_do_api.models import Task, User


class TaskDAO(DAO):
    def __init__(self):
        super().__init__()

    def insert(self, task: Task) -> int:
        return self.execute(
            "INSERT INTO public.task(id, user_id, description, state) VALUES(%s,%s,%s,%s)", 
            (task.id, task.user.id, task.description, task.state.value)
        )

    def update(self, task: Task) -> int:
        return self.execute(
            """
            UPDATE public.task
            SET user_id = %s, description = %s, state = %s
            WHERE id = %s
            """, 
            (task.user.id, task.description, task.state.value, task.id)
        )

    def delete(self, id: uuid.UUID) -> int:
        return self.execute(
            """
            DELETE FROM public.task
            WHERE id = %s
            """, 
            (id)
        )

    def get(self, id: uuid.UUID) -> Task:
        task = self.fetch_one(
            """
                SELECT t.id, description, state,
                    u.id as user_id, u.name, u.username, u.password
                FROM public.task t
                INNER JOIN public.user u on t.user_id = u.id
                WHERE t.id = %s
            """,
            (id, )
        )

        return Task(id=task[0], description=task[1], state=task[2], user=User(id=task[3], name=task[4], username=task[5], password=task[6]))

    def list(self, user_id: uuid.UUID) -> list[Task]:
        tasks = self.fetch_all(
            """
                SELECT t.id, description, state,
                    u.id as user_id, u.name, u.username, u.password
                FROM public.task t
                INNER JOIN public.user u on t.user_id = u.id
                WHERE t.user_id = %s
            """,
            (user_id, )
        )

        tasks = [Task(id=task[0], description=task[1], state=task[2], user=User(id=task[3], name=task[4], username=task[5], password=task[6])) for task in tasks]
        return tasks