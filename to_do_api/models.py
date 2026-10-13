import uuid
from enum import Enum

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class TaskManage(BaseModel):
    description: str
    state: TaskState


class User(BaseModel):
    id: uuid.UUID
    name: str
    username: str
    password: str

    @staticmethod
    def from_create(user_create: UserCreate) -> User:
        return User(
            id=uuid.uuid4(), 
            name=user_create.name, 
            username=user_create.username, 
            password=user_create.password
        )


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
    def from_create(user_id: uuid.UUID, task_create: TaskManage, user: User) -> Task:
        return Task(id=uuid.uuid4(), description=task_create.description, state=task_create.state, user=user)


class AuthResponse(BaseModel):
	access_token: str
	refresh_token: str
	user: User


class Login(BaseModel):
    username: str
    password: str