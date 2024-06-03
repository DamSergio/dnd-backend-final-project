from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    """Server config settings"""

    # Uvicorn settings
    uvicorn_app: str = config("UVICORN_APP")
    host: str = config("HOST", default="127.0.0.1")
    port: int = config("PORT", default=3001, cast=int)
    reload: bool = config("RELOAD", default=True, cast=bool)

    # Mongo Engine settings
    mongo_uri: str = config("MONGO_URI")

    # Security settings
    jwt_secret: str = config("JWT_SECRET_KEY")
    salt: bytes = config("SALT").encode()

    # Email settings
    email_host: str = config("SMTP_HOST")
    email_port: int = config("SMTP_PORT", cast=int)
    email_from: str = config("SMTP_FROM")
    email_password: str = config("SMTP_PASSWORD")

    # Firebase settings
    firabase_config: dict = {
        "apiKey": config("FIREBASE_API_KEY"),
        "authDomain": config("FIREBASE_AUTH_DOMAIN"),
        "databaseURL": config("FIREBASE_DATABASE_URL"),
        "projectId": config("FIREBASE_PROJECT_ID"),
        "storageBucket": config("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": config("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": config("FIREBASE_APP_ID"),
        "measurementId": config("FIREBASE_MEASUREMENT_ID"),
    }


CONFIG = Settings()
