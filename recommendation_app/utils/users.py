from http import HTTPStatus

import jwt
from core.config import config
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

BEARER = HTTPBearer()


async def get_user(user_credentials: HTTPAuthorizationCredentials = Security(BEARER)) -> str:
    try:
        payload = jwt.decode(
            jwt=user_credentials.credentials,
            key=config.SECRET_KEY,
            algorithms=[config.HASH_ALGORITHM],
            options={"verify_signature": False},
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid jwt token.",
        ) from None
    user_data = payload["sub"]
    user_id = user_data.get("user_id")
    return user_id
