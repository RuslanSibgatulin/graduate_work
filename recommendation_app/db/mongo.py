from typing import Optional

from core.config import config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid

mongo_client: Optional[AsyncIOMotorClient] = None


async def get_mongo() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(config.mongo_uri)
    return client


async def get_mongo_client() -> AsyncIOMotorClient:
    return mongo_client

