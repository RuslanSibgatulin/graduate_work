import logging
from http import HTTPStatus

from aiohttp import ClientSession
from core.config import config
from fastapi import HTTPException
from models.movies_list import GerneMovies, Movie


class APIMoviesService:
    @classmethod
    async def get_movies_by_(cls, genre: str = None) -> GerneMovies:
        params = {"sort": "-imdb_rating", "page[size]": 10}
        if genre is not None:
            params["filter[genre]"] = genre
        async with ClientSession() as session:
            async with session.get(config.url_movies_by_genre, params=params) as request:
                json_body = await request.json()
                if request.status == HTTPStatus.OK:
                    movies = []
                    for movie in json_body:
                        movies.append(Movie(**movie))
                    return GerneMovies(genre=genre, movies=movies)
                else:
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
                else:
                    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Something went wrong")


def get_api_movies_service() -> APIMoviesService:
    return APIMoviesService
