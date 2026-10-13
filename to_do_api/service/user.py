

import uuid

from to_do_api.dao.user import UserDAO
from to_do_api.models import User
from to_do_api.service.base import Service


class UserService(Service):
    def __init__(self):
        super().__init__()
        self.__dao = UserDAO()

    def insert(self, user: User) -> User:
        user.password = self.password_hash.hash(user.password)
        self.__dao.insert(user)

        return user

    def update(self, user: User) -> User:
        user.password = self.password_hash.hash(user.password)
        self.__dao.update(user)

        return user

    def get(self, id: uuid.UUID) -> User:
        return self.__dao.get(id=id)

    def list(self) -> list[User]:
        return self.__dao.list()

    def get_by_username(self, username: str) -> User:
        return self.__dao.get_by_username(username=username)
