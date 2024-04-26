from typing import Optional
from beanie import Document
from bson import ObjectId


class Character(Document):
    _id: ObjectId

    name: str
    gender: str
    age: int
    history: str
    picture: Optional[str]
    isAlive: bool = True

    proficiency_bonus: list

    race: str
    sub_race: Optional[str]
    character_class: str
    subclass: Optional[str]

    max_hp: int
    current_hp: int
    armor_class: int
    level: int = 1
    xp: int = 0
    speed: int
    stats: dict = {
        "str": int,
        "dex": int,
        "con": int,
        "int": int,
        "wis": int,
        "cha": int,
    }

    coins: dict = {
        "cp": int,
        "sp": int,
        "ep": int,
        "gp": int,
        "pp": int,
    }
    # items = list

    class Settings:
        name = "Characters"
