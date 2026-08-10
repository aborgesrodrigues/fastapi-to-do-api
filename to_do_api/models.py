import uuid
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID = None
    name: str
    username: str


class TaskState(Enum):
    TO_DO = 1
    DOING = 2
    DONE = 3


class Task(BaseModel):
    id: uuid.UUID = None
    description: str
    user: User
    state: TaskState
