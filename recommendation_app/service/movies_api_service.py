import logging
from http import HTTPStatus
from random import choice

from aiohttp import ClientSession
from core.config import config
from db.mongo import get_mongo_client
from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models.movies_list import Movie

logger = logging.getLogger(__name__)


class APIMoviesService:
    def __init__(
            self,
            mongo: AsyncIOMotorClient,
    ) -> None:
        self.mongo_db = mongo[config.mongo_db]

    async def get_base_movies_for_(self, user_id: str) -> list[Movie]:
        params = {"sort": "-imdb_rating", "page[size]": "20"}
        collection = self.mongo_db[config.mongo_user_collection]
        user_movies_info = await collection.find_one({"user_id": user_id})
        genres = user_movies_info.get("genres")
        if genres:
            genre = choice(genres)
            params["filter[genre]"] = genre
        movies = user_movies_info.get("movies")
        if movies:
            params["exclude"] = ";".join(list(movies.keys()))
        async with ClientSession() as session:
            async with session.get(config.url_movies_by_genre, params=params) as request:
                json_body = await request.json()
                if request.status == HTTPStatus.OK:
                    movies = []
                    for movie in json_body:
                        movies.append(Movie(**movie))

                    return movies

                logger.error(
                    f"Movies api response with code {request.status}", extra=json_body
                )
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Something went wrong")

    @classmethod
    async def get_movies_by_id(cls, movies_id: list[str]) -> list[Movie]:
        params = {"ids": ",".join(movies_id)}
        async with ClientSession() as session:
            async with session.get(config.url_movies_name, params=params) as request:
                json_body = await request.json()
                if request.status == HTTPStatus.OK:
                    movies = []
                    for movie in json_body:
                        movies.append(Movie(**movie))
                    return movies

                logger.error(
                    msg=f"Movies api response with code {request.status}", extra=json_body
                )
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Something went wrong")


def get_api_movies_service(
        mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> APIMoviesService:
    return APIMoviesService(mongo=mongo_storage)
