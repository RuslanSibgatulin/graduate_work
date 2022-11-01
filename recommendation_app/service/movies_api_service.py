import logging
from http import HTTPStatus

from aiohttp import ClientSession
from core.config import config
from fastapi import HTTPException
from models.movies_list import Movie

logger = logging.getLogger(__name__)


class APIMoviesService:
    @classmethod
    async def get_movies_by_(cls, genre: str = None) -> list[Movie]:
        params = {"sort": "-imdb_rating", "page[size]": "20"}
        if genre is not None:
            params["filter[genre]"] = genre
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


def get_api_movies_service() -> APIMoviesService:
    return APIMoviesService
