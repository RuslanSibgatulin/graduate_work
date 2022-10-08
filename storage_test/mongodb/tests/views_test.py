import random
from pprint import pprint

import pytest

pytestmark = pytest.mark.asyncio


# @pytest.mark.skip(reason="Insert disabled")
@pytest.mark.parametrize(
    "users_count",
    [1000, 10000, 100000, 100000, 100000, 100000, 89000]
)
async def test_insert_users_with_views(
    mongo_db, users_list, movies_list, users_count
):
    pprint(f"Fill views collection. {users_count} docs. ")
    max_viewed = 50

    users_with_views = random.choices(users_list, k=users_count)
    viewed_movies = random.choices(movies_list, k=max_viewed)
    result = await mongo_db["views"].insert_many(
        [
            {
                "user_id": user,
                "viewed": random.choices(
                    viewed_movies, k=random.randrange(1, max_viewed)
                ),

            } for user in users_with_views
        ]
    )

    # Проверка результата
    assert len(result.inserted_ids) == users_count


@pytest.mark.parametrize(
    "attempt",
    range(10)
)
async def test_user_views_similarity(
    mongo_db, get_random_user_views, get_users_views_count, attempt
):
    user_views = get_random_user_views
    pprint(f"Get random user profile from {get_users_views_count} docs")
    pprint(f"User profile: {user_views}")
    cursor = mongo_db["views"].aggregate([
        {
            "$match": {
                "viewed": {"$in": user_views}
            }
        },
        {
            "$project":
            {
                "viewed": 1,
                "similarity":
                {
                    "$divide":
                    [
                        {
                            "$size":
                            {
                                "$setIntersection":
                                [
                                    "$viewed",
                                    user_views
                                ]
                            }
                        },
                        len(user_views)
                    ]
                }
            }
        },
        {
            "$match": {
                "similarity": {"$gte": 0.5}
            }
        },
        {
            "$unwind": "$viewed"
        },
        {
            "$match": {"viewed": {"$nin": user_views}}
        },
        {
            "$group": {"_id": "null", "movies": {"$addToSet": "$viewed"}}
        },
        {
            "$project": {"_id": 0, "offer": "$movies"}
        }
    ])
    document = await cursor.to_list(length=1)
    offer = document[0]["offer"]
    pprint(f"Offer: {offer}")
    assert not (set(user_views) & set(offer))
