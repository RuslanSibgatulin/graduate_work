from typing import Any

import aioredis
import orjson


class RedisCache:
    def __init__(self, redis_url: str) -> None:
        self.url = redis_url
        self.source = aioredis.from_url(redis_url)

    @staticmethod
    def format_key(key_title, **kwargs) -> str:
        params = ["{0}::{1}".format(k, v) for k, v in kwargs.items()]
        return "::".join([key_title, *params])

    async def get(self, key: str) -> Any:
        value = await self.source.get(key)
        if value is None:
            return None

        return orjson.loads(value)

    async def set(self, key: str, value: Any) -> None:
        await self.source.set(
            key,
            orjson.dumps(value)
        )

    async def close(self) -> None:
        await self.source.close()
