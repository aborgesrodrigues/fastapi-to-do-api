import uuid
from enum import Enum

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.UUID = None
    name: str
    username: str


class TaskState(Enum):
    TO_DO = "TO_DO"
    DOING = "DOING"
    DONE = "DONE"


class Task(BaseModel):
    id: uuid.UUID = None
    description: str
    user: User = None
    state: TaskState
