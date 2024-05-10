from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User
from app.models.character import Character
from config import CONFIG

from contextlib import asynccontextmanager
from beanie import init_beanie


@asynccontextmanager
async def connect_to_mongo(app: FastAPI):
    app = AsyncIOMotorClient(CONFIG.mongo_uri)

    # TODO: Add document_models to the list below
    await init_beanie(app.dnd_app, document_models=[User, Character])
    print("Connected to MongoDB")

    yield
    print("Disconnected from MongoDB")
