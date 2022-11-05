from http import HTTPStatus

from aiohttp import ClientSession
from core.config import fake_movies_response
from models.models import Movie, Token


async def get_fake_recommender_movies(token: Token) -> list[Movie]:
    return [Movie(**movie) for movie in fake_movies_response]


async def get_recommender_movies(url: str, token: Token) -> list[Movie]:
    headers = {"Authorization": f"Bearer {token.access_token}"}
    try:
        async with ClientSession(headers=headers) as session:
            async with session.get(url) as request:
                json_body = await request.json()
                if request.status == HTTPStatus.OK:
                    return [Movie(**movie) for movie in json_body]

                print(request.status, json_body)
                return []
    except Exception:
        return []
