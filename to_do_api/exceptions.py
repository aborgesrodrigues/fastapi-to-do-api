class UserAlreadyExistsError(Exception):
    def __init__(self, username: str):
        super().__init__(f"username '{username}' already exists")
        self.username = username
