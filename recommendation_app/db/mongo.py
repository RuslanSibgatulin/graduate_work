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


async def init_collections():
    client = await get_mongo_client()
    db = client[config.MONGO_DB]
    for collection in config.get_collections():
        try:
            await db.create_collection(collection)
        except CollectionInvalid:
            pass
