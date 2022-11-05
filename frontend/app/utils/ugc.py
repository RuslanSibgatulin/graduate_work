from http import HTTPStatus

from aiohttp import ClientSession
from models.models import Token, MovieLike, MovieProgress
from core.config import ugc_like_url, ugc_progress_url


async def set_ugc_like(token: Token, data: MovieLike) -> HTTPStatus:
    headers = {"Authorization": f"Bearer {token.access_token}"}
    try:
        async with ClientSession(headers=headers) as session:
            async with session.post(ugc_like_url, json=data.dict()) as request:
                return request.status

    except Exception:
        return HTTPStatus.INTERNAL_SERVER_ERROR


async def set_ugc_progress(token: Token, data: MovieProgress) -> bool:
    headers = {"Authorization": f"Bearer {token.access_token}"}
    try:
        async with ClientSession(headers=headers) as session:
            async with session.post(
                ugc_progress_url,
                json=data.dict()
            ) as request:
                return request.status

    except Exception:
        return HTTPStatus.INTERNAL_SERVER_ERROR
