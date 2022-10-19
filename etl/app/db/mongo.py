import logging

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class MongoInterface:
    def __init__(self, mongodb_url: str, dbname: str) -> None:
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[dbname]

    def __del__(self):
        pass

    async def add_movie_to_profile(
        self, user_id: str, movie_id: str, rating: int = None
    ) -> bool:
        result = await self.db["profiles"].update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {f"viewed.{movie_id}": rating}
            },
            upsert=True
        )
        return result.acknowledged
