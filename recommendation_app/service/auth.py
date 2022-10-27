from typing import Any

from aiohttp.client import ClientSession
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from core.config import config


oauth2_scheme = HTTPBearer()


async def get_genres_and_validate(
        token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
) -> list[str]:
    genres = await AuthService.validate_token_and_get_genres(token)
    return genres


class AuthService:
    @classmethod
    async def validate_token_and_get_genres(cls, token: HTTPAuthorizationCredentials) -> Any:
        headers = {"Authorization": f"Bearer {token.credentials}"}
        async with ClientSession(headers=headers) as session:
            async with session.get(config.USER_GENRES_CHECK_URL) as r:
                json_body = await r.json()
                if r.status == status.HTTP_200_OK:
                    return json_body["genres"]
                elif r.status == status.HTTP_403_FORBIDDEN:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail=json_body["message"]
                    )
                elif r.status == status.HTTP_401_UNAUTHORIZED:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail=json_body["msg"]
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=json_body
                    )
        return None
