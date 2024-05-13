from beanie import Document, Link, BackLink
from typing import Optional, List
from pydantic import Field
from bson import ObjectId

from app.models.character import CreateCharacter


class User(Document):
    _id: ObjectId

    username: str
    email: str
    password: str
    profile_picture: Optional[str]
    verfied: bool = False
    rol: str = "user"
    characters: Optional[List[Link["Character"]]] = []

    refresh_token: str = ""

    @property
    def jwt_subject(self):
        return {"email": self.email}

    @classmethod
    async def by_email(cls, email: str):
        return await cls.find_one({"email": email})

    class Settings:
        name = "Users"


class Character(Document, CreateCharacter):
    _id: ObjectId
    user: BackLink[User] = Field(original_field="characters")

    level: int = 1

    abilities: Optional[List[str]] = []
    speels: Optional[List[str]] = []

    class Settings:
        name = "Characters"
