import orjson
from core.config import config
from db.mongo import get_mongo_client
from fastapi import Depends
from models.movies_list import Movie
from motor.motor_asyncio import AsyncIOMotorClient
from service.grpc.client import GRPCModelClient
from service.movies_api_service import APIMoviesService
from utils.models import Movie as MovieDC


class MoviesService:
    def __init__(
        self,
        mongo: AsyncIOMotorClient,
    ) -> None:
        self.mongo_db = mongo[config.mongo_db]
        self.grpc_client = GRPCModelClient
        self.api_client = APIMoviesService

    async def get_movies_for(self, user_id: str) -> list[Movie]:
        collection = self.mongo_db[config.mongo_user_collection]
        user_movies_info = await collection.find_one({"user_id": user_id})
        if not user_movies_info:
            return []

        movies = user_movies_info[
            "movies"
        ]  # dict { movie_id : { timestamp: float, score: float } }
        if isinstance(movies, str):
            movies = orjson.loads(movies)
        obj_list = []
        for movie_id, info in movies.items():
            obj_list.append(
                MovieDC(
                    id=movie_id,
                    timestamp=info.get("timestamp"),
                    score=info.get("score"),
                )
            )
        obj_list.sort(key=lambda obj_: obj_.timestamp)
        viewed_movie_ids = dict.fromkeys([movie.id for movie in obj_list])
        recs_response = await self.grpc_client.get_movies(
            user_id, list(viewed_movie_ids)[-10:]
        )
        recs_movie_ids = [obj_.movie_id for obj_ in recs_response.movies]
        top_movie_ids = [
            movie_id for movie_id in recs_movie_ids if movie_id not in viewed_movie_ids
        ][:5]
        movies_data = await self.api_client.get_movies_by_id(top_movie_ids)
        return movies_data


def get_movies_service(
    mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> MoviesService:
    return MoviesService(mongo=mongo_storage)
