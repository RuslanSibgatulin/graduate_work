from fastapi import APIRouter, Request, status
from fastapi.security import HTTPBearer
from models.models import Token, MovieLike, MovieProgress
from utils.ugc import set_ugc_like, set_ugc_progress

router = APIRouter(tags=["Actions"])
bearer = HTTPBearer()


@router.post("/like", status_code=status.HTTP_201_CREATED)
async def like_movie(
    like: MovieLike,
    request: Request
):
    token = Token(**request.session["auth_token"])
    await set_ugc_like(token, like)


@router.post(
    "/viewed",
    status_code=status.HTTP_201_CREATED
)
async def viewed_movie(
    progress: MovieProgress,
    request: Request
):
    token = Token(**request.session["auth_token"])
    await set_ugc_progress(token, progress)
