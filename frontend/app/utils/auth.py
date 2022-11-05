from http import HTTPStatus

import jwt
from aiohttp import ClientSession
from core.config import auth_url, fake_token
from models.models import Token


async def refresh_token():
    pass


def decode_token(token: Token):
    return jwt.decode(
        token.access_token,
        options={"verify_signature": False}
    )


async def get_fake_access_token(login: str, password: str) -> Token | None:
    return Token.parse_obj(fake_token)


async def get_access_token(login: str, password: str) -> Token | None:
    data = {"login": login, "password": password}
    async with ClientSession() as session:
        async with session.post(auth_url, json=data) as request:
            if request.status == HTTPStatus.OK:
                json_body = await request.json()
                return Token.parse_obj(json_body)
            return None
