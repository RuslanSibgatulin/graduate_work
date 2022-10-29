from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import config
from db.mongo import get_mongo_client
from models.movies_list import Movie
from service.grpc.client import GRPCModelClient
from service.movies_api_service import APIMoviesService
from utils.models import Movie as MovieDC


class MoviesService:
    def __init__(
            self,
            mongo: AsyncIOMotorClient,
    ) -> None:
        self.mongo_db = mongo[config.MONGO_DB]
        self.grpc_client = GRPCModelClient
        self.api_client = APIMoviesService

    async def get_movies_for(self, user_id: str) -> list[Movie]:
        collection = self.mongo_db[config.MONGO_USER_COLLECTION]
        user_movies_info = await collection.find_one({"user_id": user_id})
        movies = user_movies_info["movies"]  # dict { movie_id : { timestamp: float, score: float } }
        obj_list = []
        for movie_id, info in movies.items():
            obj_list.append(MovieDC(
                id=movie_id, timestamp=info.get("timestamp"), score=info.get("score")
            ))
        obj_list.sort(key=lambda obj_: obj_.timestamp, reverse=True)
        movies_id = [movie.id for movie in obj_list[:10]]
        new_movies_ids_response = await self.grpc_client.get_movies(user_id, movies_id)
        new_movies_id = [obj_.movie_id for obj_ in new_movies_ids_response.movies]
        movies_data = await self.api_client.get_movies_by_id(new_movies_id)
        return movies_data


def get_movies_service(
        mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client)
) -> MoviesService:
    return MoviesService(mongo=mongo_storage)
