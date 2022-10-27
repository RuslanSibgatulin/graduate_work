import asyncio

from fastapi import APIRouter, Depends, Security, status

from models.movies_list import GerneMovies
from service.auth import get_genres_and_validate
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
async def get_base_genres(
        genres: list[str] = Security(get_genres_and_validate),
        service: MoviesService = Depends(get_movies_service)
) -> list[GerneMovies]:
    tasks = []
    for genre in genres:
        task = asyncio.create_task(service.get_movies_by_(genre))
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    return MovieProcessor.get_genre_movies(result)
