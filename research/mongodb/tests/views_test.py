import random
from pprint import pprint

import pytest
from pymongo import ReturnDocument

pytestmark = pytest.mark.asyncio


@pytest.mark.skip(reason="Disabled")
@pytest.mark.parametrize(
    "count,genre",
    [
        (1000, "Animation"),
        (1000, "Drama"),
        (1000, "Action"),
        (1000, "Fantasy"),
        (1000, "Thriller"),
        (1000, "Adventure"),
        (1000, "Crime"),
        (1000, "Romance"),
        (1000, "Documentary"),
        (1000, "Sci-Fi")
    ],
    indirect=["genre"]
)
async def test_update_user_views(
    mongo_db, users_list, movies_by_genre, count, genre
):
    pprint(f"Fill views collection. {count} docs with {genre}")
    max_viewed = 20

    users_with_views = random.choices(users_list, k=count)

    for user in users_with_views:
        viewed_movies = random.choices(movies_by_genre, k=max_viewed)
        result = await mongo_db["views"].find_one_and_update(
            {
                "user_id": user
            },
            {
                "$addToSet":
                {
                    "viewed": {"$each": viewed_movies}
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        # Проверка результата
        assert set(result["viewed"]) & set(viewed_movies)


@pytest.mark.parametrize(
    "count,genre",
    [
        (10000, "Animation"),
        (10000, "Drama"),
        (10000, "Action"),
        (10000, "Fantasy"),
        (10000, "Thriller"),
        (10000, "Adventure"),
        (10000, "Crime"),
        (10000, "Romance"),
        (10000, "Documentary"),
        (10000, "Sci-Fi")
    ]
)
async def test_insert_user_views(
    mongo_db, users_list, movies_by_genre, count, genre
):
    pprint(f"Fill views collection. {count} docs with genre {genre}")
    max_viewed = 20

    users_with_views = random.choices(users_list, k=count)
    result = await mongo_db["views"].insert_many(
        [
            {
                "user_id": user,
                "viewed": random.choices(
                    movies_by_genre, k=random.randrange(3, max_viewed)
                ),

            } for user in users_with_views
        ]
    )

    # Проверка результата
    assert len(result.inserted_ids) == count


# @pytest.mark.skip(reason="Disabled")
@pytest.mark.parametrize(
    "attempt",
    range(10)
)
async def test_user_views_similarity(
    mongo_db, get_random_user_views,
    get_users_views_count, attempt, pandas_movies
):
    user_views = get_random_user_views
    pprint(f"Get random user profile from {get_users_views_count} docs")

    user_movies = pandas_movies.query("index in @user_views")
    user_genres = [
        genres.split("|") for genres in list(user_movies.loc[:, "genres"])
    ]
    user_genres = list(set(sum(user_genres, [])))
    pprint("User views:")
    pprint(user_movies)

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
            "$sort": {
                "similarity": -1
            }
        },
        {
            "$limit": 10
        },
        {
            "$unwind": "$viewed"
        },
        {
            "$match": {"viewed": {"$nin": user_views}}
        },
        {
            "$sample": {"size": 50}
        },
        {
            "$group": {"_id": "null", "movies": {"$addToSet": "$viewed"}}
        },
        {
            "$project": {"_id": 0, "offer": "$movies"}
        }
    ])
    document = await cursor.to_list(length=1)
    offer = document[0]["offer"] if len(document) else []
    pprint("Offer with max similarity:")
    pprint(pandas_movies.query("index in @offer"))
    assert len(offer)
    assert not (set(user_views) & set(offer))
