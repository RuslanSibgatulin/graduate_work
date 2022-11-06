import logging
import time

from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger(__name__)


class MongoInterface:
    def __init__(self, mongodb_url: str, dbname: str) -> None:
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client[dbname]

    def __del__(self):
        pass

    async def add_like_to_profile(
        self, user_id: str, movie_id: str, score: int
    ) -> bool:
        result = await self.db["profiles"].update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {
                    f"movies.{movie_id}.timestamp": int(time.time()),
                    f"movies.{movie_id}.score": score
                }
            },
            upsert=True
        )
        return result.acknowledged

    async def add_view_to_profile(
        self, user_id: str, movie_id: str, timestamp: int
    ) -> bool:
        result = await self.db["profiles"].update_one(
            {
                "user_id": user_id
            },
            {
                "$set": {f"movies.{movie_id}.timestamp": timestamp}
            },
            upsert=True
        )
        return result.acknowledged
