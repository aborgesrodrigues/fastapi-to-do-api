class UserAlreadyExistsError(Exception):
    def __init__(self, username: str):
        super().__init__(f"username '{username}' already exists")
        self.username = username


class LoginError(Exception):
    def __init__(self, username: str):
        super().__init__("username or password incorrect")
        self.username = username


class UnauthorizedError(Exception):
    def __init__(self, username: str):
        super().__init__(f"username '{username}' has no permission")
        self.username = username