from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import config
from db.mongo import get_mongo_client
from models.movies_list import Movie
from service.grpc.client import GRPCModelClient
from service.movies_api_service import APIMoviesService


class MoviesService:
    def __init__(
            self,
            mongo: AsyncIOMotorClient,
    ) -> None:
        self.mongo_db = mongo[config.MONGO_DB]
        self.grpc_client = GRPCModelClient
        self.api_client = APIMoviesService

    async def get_movies_for(self, user_id: str) -> list[Movie]:
        # collection = self.mongo_db[config.MONGO_USER_COLLECTION]
        # user_movies_info = await collection.find_one({"user_id": user_id})
        # movies_id = user_movies_info["movies"]
        movies_id = [f"movie_id_{num+1}" for num in range(5)]
        new_movies_ids_response = await self.grpc_client.get_movies(user_id, movies_id)
        movies_data = await self.api_client.get_movies_by_id(
            obj_.movie_id for obj_ in new_movies_ids_response.movies
        )
        return movies_data


def get_movies_service(
        mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client)
) -> MoviesService:
    return MoviesService(mongo=mongo_storage)