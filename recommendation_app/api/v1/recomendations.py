from random import choice

from fastapi import APIRouter, Depends, Security, status
from models.movies_list import Movie
from service.auth import get_genres_and_validate
from service.movies_api_service import APIMoviesService, get_api_movies_service
from service.movies_service import MoviesService, get_movies_service

router = APIRouter(tags=["Recommendations"])


@router.get(
    "/base",
    summary="Get movies by genre.",
    description="Get movies for user with user's favorite genres.",
    response_model=list[Movie],
    status_code=status.HTTP_200_OK,
)
async def get_base_movies(
        user_info: dict = Security(get_genres_and_validate),
        service: APIMoviesService = Depends(get_api_movies_service)
) -> list[Movie]:
    genres = user_info["genres"]
    if genres:
        genre = choice(genres)
    else:
        genre = None
    movies = await service.get_movies_by_(genre)
    return movies


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
