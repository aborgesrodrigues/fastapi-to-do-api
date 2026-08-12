import uuid
from enum import Enum

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: uuid.UUID = None
    name: str
    username: str


class TaskCreate(BaseModel):
    id: uuid.UUID = None
    description: str
    state: TaskState


class User(BaseModel):
    id: uuid.UUID
    name: str
    username: str

    @staticmethod
    def from_create(user_create: UserCreate) -> User:
        return User(id=uuid.uuid4(), name=user_create.name, username=user_create.username)


class TaskState(Enum):
    TO_DO = "TO_DO"
    DOING = "DOING"
    DONE = "DONE"


class Task(BaseModel):
    id: uuid.UUID
    description: str
    user: User
    state: TaskState

    @staticmethod
    def from_create(user_id: uuid.UUID, task_create: TaskCreate) -> Task:
        return Task(id=uuid.uuid4(), description=task_create.description, state=task_create.state, user=User(id=user_id, name="", username=""))
