import bcrypt
from config import CONFIG


def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), CONFIG.salt).decode()
