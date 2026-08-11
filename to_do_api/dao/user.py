
from to_do_api.dao.dao import DAO
from to_do_api.models import User


class UserDAO(DAO):
    def __init__(self):
        super().__init__()

    def insert(self, user: User) -> int:
        return self.execute("INSERT INTO public.user(id, username, name) VALUES(%s,%s,%s)", (user.id, user.username, user.name))

    def list(self) -> list[User]:
        users = self.fetch_all("SELECT id, name, username FROM public.user")

        users = [User(id=user[0], name=user[1], username=user[2]) for user in users]
        return users