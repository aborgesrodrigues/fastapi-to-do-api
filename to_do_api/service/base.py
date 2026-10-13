from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class Service:
    def __init__(self):
        self.password_hash = password_hash
