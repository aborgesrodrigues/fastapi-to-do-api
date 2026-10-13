
from psycopg2.errors import UniqueViolation

from to_do_api.dao.dao import DAO
from to_do_api.exceptions import UserAlreadyExistsError
from to_do_api.models import User


class UserDAO(DAO):
    def __init__(self):
        super().__init__()

    def insert(self, user: User) -> int:
        try:
            return self.execute(
                """
                INSERT INTO public.user(id, username, name, password) VALUES(%s,%s,%s, %s)
                """, 
                (user.id, user.username, user.name, user.password)
            )
        except UniqueViolation:
            raise UserAlreadyExistsError(username=user.username)
        

    def list(self) -> list[User]:
        users = self.fetch_all("SELECT id, name, username FROM public.user")

        users = [User(id=user[0], name=user[1], username=user[2]) for user in users]
        return users

    def get(self, username: str) -> User:
        user = self.fetch_one(
            """
            SELECT id, name, username, password 
            FROM public.user u 
            WHERE u.username = %s
            """, (username, ))

        return User(id=user[0], name=user[1], username=user[2], password=user[3])
