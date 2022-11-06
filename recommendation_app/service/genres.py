
from core.config import config
from db.mongo import get_mongo_client
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient


class GenreService:
    def __init__(
        self,
        mongo: AsyncIOMotorClient,
    ) -> None:
        self.mongo_db = mongo[config.mongo_db]

    async def add_genre(self, user_id: str, genre_name: str) -> bool:
        collection = self.mongo_db[config.mongo_user_collection]
        result = await collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"genres": genre_name}},
            upsert=True
        )
        return result.acknowledged


def get_genres_service(
    mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> GenreService:
    return GenreService(mongo=mongo_storage)
