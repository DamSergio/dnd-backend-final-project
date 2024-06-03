import pytest

from motor.motor_asyncio import AsyncIOMotorClient
from app.models.models_in_db import User, Character, Campaign
from config import CONFIG

from contextlib import asynccontextmanager
from beanie import init_beanie


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@asynccontextmanager
async def connect_to_mongo(app):
    app = AsyncIOMotorClient(CONFIG.mongo_uri)

    await init_beanie(app.dnd_app, document_models=[User, Character, Campaign])
    print("Connected to MongoDB")

    yield
    print("Disconnected from MongoDB")
