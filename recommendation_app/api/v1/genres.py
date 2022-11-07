from fastapi import APIRouter, Depends, Security, status
from models.genres import Genre
from service.auth import get_current_user
from service.genres import GenreService, get_genres_service

router = APIRouter(tags=["Genres"])


@router.post(
    "/genres",
    summary="Add user's genre.",
    description="Add genre to user's favorite genres list.",
    status_code=status.HTTP_200_OK,
)
async def get_base_movies(
        genre_name: Genre,
        user_info: dict = Security(get_current_user),
        service: GenreService = Depends(get_genres_service)
) -> None:
    user_id = user_info["user_id"]
    await service.add_genre(user_id, genre_name)
