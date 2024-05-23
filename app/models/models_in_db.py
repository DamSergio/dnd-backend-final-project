from beanie import Document, Link, BackLink
from typing import Optional, List
from pydantic import Field
from bson import ObjectId

from app.models.character import CreateCharacter
from app.models.campaign import CreateCampaign
from app.models.invitation import Invitation


class User(Document):
    _id: ObjectId

    username: str
    email: str
    password: str
    profile_picture: Optional[str]
    verfied: bool = False
    rol: str = "user"

    characters: Optional[List[Link["Character"]]] = []
    my_campaigns: Optional[BackLink["Campaign"]] = Field(
        original_field="dungeon_master"
    )

    invitations: Optional[List[Invitation]] = []

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
    picture: Optional[str] = ""

    abilities: Optional[List[str]] = []
    spells: Optional[List[str]] = []

    campaigns: Optional[List[BackLink["Campaign"]]] = Field(original_field="players")

    class Settings:
        name = "Characters"


class Campaign(Document, CreateCampaign):
    _id: ObjectId

    dungeon_master: Link["User"]
    players: Optional[List[Link[Character]]] = []

    class Settings:
        name = "Campaigns"
