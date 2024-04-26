from pydantic import BaseModel
from beanie import Document
from typing import Optional
from bson import ObjectId
from app.models.character import Character


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class LoginUser(BaseModel):
    email: str
    password: str


class User(Document):
    _id: ObjectId

    username: str
    email: str
    password: str
    profile_picture: Optional[str]
    verfied: bool = False
    rol: str = "user"
    characters: list["Character"] = []

    @property
    def jwt_subject(self):
        return {"email": self.email}

    @classmethod
    async def by_email(cls, email: str):
        return await cls.find_one({"email": email})

    class Settings:
        name = "Users"
