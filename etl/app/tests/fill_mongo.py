import asyncio
import random
import time
import uuid

from mongo import MongoInterface


async def fill_mogodb() -> None:
    mi = MongoInterface("127.0.0.1:27017", "recom_db")
    for _ in range(10):
        user = str(uuid.uuid4())
        for _ in range(random.randrange(1, 5)):
            movie = str(uuid.uuid4())
            await mi.add_view_to_profile(user, movie, int(time.time()))


async def fill_profile(user: str) -> None:
    mi = MongoInterface("127.0.0.1:27017", "recom_db")
    movie = str(uuid.uuid4())
    await mi.add_view_to_profile(user, movie, int(time.time()))
    await mi.add_like_to_profile(user, movie, 5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fill_profile("908e33da-6f57-40a5-a8cf-5722dbeed1dc"))  # root user
