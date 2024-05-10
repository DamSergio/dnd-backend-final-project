from typing import Optional, List
from beanie import Document
from bson import ObjectId
from pydantic import BaseModel


class Race(BaseModel):
    name: str
    icon: str
    subRace: Optional[str]


class Class(BaseModel):
    name: str
    icon: str


class Skill(BaseModel):
    name: str
    description: str


class Trait(BaseModel):
    name: str
    description: str


class Item(BaseModel):
    name: str
    quantity: int


class Stats(BaseModel):
    str: int
    dex: int
    con: int
    wis: int
    cha: int
    int: int


class Coins(BaseModel):
    cp: int
    sp: int
    ep: int
    gp: int
    pp: int


class CreateCharacter(BaseModel):
    name: str
    gender: str
    age: int

    background: str
    alignment: str

    personality_traits: Optional[str]
    ideals: Optional[str]
    bonds: Optional[str]
    flaws: Optional[str]
    history: Optional[str]

    character_race: Race
    character_class: Class

    hit_points: int
    armor_class: int
    speed: int
    saving_throws: List[str] = []
    armor_proficiencies: Optional[List[str]] = []
    weapon_proficiencies: Optional[List[str]] = []
    tool_proficiencies: Optional[List[str]] = []

    stats: Stats
    coins: Coins

    skills: List[Skill]
    traits: List[Trait]
    items: List[Item]
    languages: List[str]


class Character(Document, CreateCharacter):
    _id: ObjectId

    abilities: Optional[List[str]] = []
    speels: Optional[List[str]] = []

    class Settings:
        name = "Characters"
