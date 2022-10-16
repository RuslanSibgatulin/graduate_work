import random
from pprint import pprint

import pytest
from pymongo import ReturnDocument

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "count,genre",
    [
        (10, "Action")
    ]
)
async def test_update_ratings(
    mongo_db, users_list, movies_by_genre, count, genre
):
    max_viewed = 10

    users_with_likes = random.choices(users_list, k=count)
    users_likes = [None, 5, 4, 3]
    result = await mongo_db["ratings"].insert_many(
        [
            {
                "user_id": user,
                "ratings": dict(
                    [
                        (
                            str(movie), random.choice(users_likes)
                        ) for movie in random.sample(
                            movies_by_genre, k=random.randrange(3, max_viewed)
                        )
                    ]
                )
            } for user in users_with_likes
        ]
    )

    # Проверка результата
    assert len(result.inserted_ids) == count
