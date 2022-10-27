import random
from pprint import pprint

import pytest
from pymongo import ReturnDocument

pytestmark = pytest.mark.asyncio


# @pytest.mark.skip(reason="Insert disabled")
@pytest.mark.parametrize(
    "count",
    [7, 6, 5, 4, 3, 2]
)
async def test_insert_user_view_progress(
    mongo_db, users_list, movies_list, count
):
    pprint(f"Inc progress collection. {count} docs. ")

    user = random.choice(users_list)
    view_movie = random.choice(movies_list)

    for i in range(count):
        doc = await mongo_db["views"].find_one_and_update(
            {'user_id': user},
            {'$inc': {f'viewed.{view_movie}': 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
    # Проверка результата
    assert doc["viewed"][view_movie] == count
