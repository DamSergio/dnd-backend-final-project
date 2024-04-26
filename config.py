from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    """Server config settings"""

    # Uvicorn settings
    uvicorn_app: str = config("UVICORN_APP")
    host: str = config("HOST", default="127.0.0.1")
    port: int = config("PORT", default=5000, cast=int)
    reload: bool = config("RELOAD", default=True, cast=bool)

    # Mongo Engine settings
    mongo_uri: str = config("MONGO_URI")

    # Security settings
    jwt_secret: str = config("JWT_SECRET_KEY")
    salt: bytes = config("SALT").encode()


CONFIG = Settings()
