import asyncio

from fastapi import APIRouter, Depends, Security, status
from models.movies_list import GerneMovies, Movie
from service.auth import get_genres_and_validate
from service.movies_api_service import APIMoviesService, get_api_movies_service
from service.movies_service import MoviesService, get_movies_service
from utils.movie_process import MovieProcessor

router = APIRouter(tags=["Recommendations"])


@router.get(
    "/base",
    summary="Get movies by genre.",
    description="Get movies for user with user's favorite genres.",
    response_model=list[GerneMovies],
    status_code=status.HTTP_200_OK,
)
async def get_base_movies(
        user_info: dict = Security(get_genres_and_validate),
        service: APIMoviesService = Depends(get_api_movies_service)
) -> list[GerneMovies]:
    tasks = []
    for genre in user_info["genres"]:
        task = asyncio.create_task(service.get_movies_by_(genre))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    return MovieProcessor.get_genre_movies(result)


@router.get(
    "/model",
    summary="Get movies from model.",
    description="Get movies for user.",
    response_model=list[Movie],
    status_code=status.HTTP_200_OK,
)
async def get_model_movies(
        user_info: dict = Security(get_genres_and_validate),
        service: MoviesService = Depends(get_movies_service)
) -> list[Movie]:
    user_id = user_info["user_id"]
    movies = await service.get_movies_for(user_id)
    return movies
