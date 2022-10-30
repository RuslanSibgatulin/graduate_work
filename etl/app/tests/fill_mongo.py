import asyncio
import random
import time
import uuid

from db.mongo import MongoInterface


async def fill_mogodb() -> None:
    mi = MongoInterface("127.0.0.1:27019", "recom_db")
    for _ in range(10):
        user = str(uuid.uuid4())
        for _ in range(random.randrange(1, 5)):
            movie = str(uuid.uuid4())
            await mi.add_view_to_profile(user, movie, int(time.time()))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fill_mogodb())
