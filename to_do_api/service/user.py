

from to_do_api.dao.user import UserDAO
from to_do_api.models import User


class UserService:
    def __init__(self):
        self.__dao = UserDAO()

    def insert(self, user: User) -> User:
        self.__dao.insert(user)

        return user

    def list(self) -> list[User]:
        return self.__dao.list()