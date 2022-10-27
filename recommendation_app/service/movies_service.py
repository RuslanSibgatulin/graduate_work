from http import HTTPStatus

from aiohttp import ClientSession
from fastapi import HTTPException

from core.config import config
from models.movies_list import GerneMovies, Movie


class MoviesService:

    URL_MOVIES_NAME = "http://127.0.0.1/api/v1/film/names"

    @staticmethod
    async def get_movies_by_(genre: str) -> GerneMovies:
        params = {"filter[genre]": genre, "sort": "-imdb_rating", "page[size]": 10}
        async with ClientSession() as session:
            async with session.get(config.URL_MOVIES_BY_GENRES, params=params) as request:
                json_body = await request.json()
                if request.status == HTTPStatus.OK:
                    movies = []
                    for movie in json_body:
                        movies.append(Movie(**movie))
                    return GerneMovies(genre=genre, movies=movies)
                else:
                    raise HTTPException(status_code=request.status, detail="Film not found")

    async def get_movies_names(self, movies_id: list[str]) -> list[str]:
        pass


def get_movies_service() -> MoviesService:
    return MoviesService()
