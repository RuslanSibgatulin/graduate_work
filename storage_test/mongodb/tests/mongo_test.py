import random

import pytest
from faker import Faker

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'limit',
    [10000, 100000, 1000000]
)
async def test_insert_movies_likes(mongo_db, users_list, movies_list, limit):
    print(f'Fill likes collection. {limit} docs. ', end='\n')
    n = 0
    while n < limit:
        movies_with_likes = random.choices(movies_list, k=1000)
        result = await mongo_db['likes'].insert_many(
            [
                {
                    'movie_id': movie,
                    'user_id': random.choice(users_list),
                    'rating': random.randrange(0, 10)

                } for movie in movies_with_likes
            ]
        )
        n += len(result.inserted_ids)
        percent = int(n / limit * 100)
        print(f'\r\tInserted docs | {n} | {percent}%', end="\r")

    # Проверка результата
    assert n == limit


async def test_insert_review_likes(mongo_db, users_list, movies_list):
    # Fill reviews collection
    fake = Faker()
    movies_with_review = random.choices(
        movies_list, k=len(movies_list) // 10
    )
    result = await mongo_db['reviews'].insert_many(
        [
            {
                'author': {
                    'username': fake.user_name(),
                    'user_id': random.choice(users_list)
                },
                'time': fake.date_time_this_year(),
                'movie_id': movie,
                'rating': random.randrange(0, 11),
                'text': fake.text()

            } for movie in movies_with_review
        ]
    )
    assert len(result.inserted_ids) == len(movies_list) // 10

    # Fill review likes
    reviews_ids = result.inserted_ids
    result = await mongo_db['likes'].insert_many(
        [
            {
                'review_id': review,
                'user_id': random.choice(users_list),
                'rating': random.randrange(0, 11)

            } for review in random.choices(reviews_ids, k=len(reviews_ids) // 2)
        ]
    )

    assert len(result.inserted_ids) == len(reviews_ids) // 2


@pytest.mark.parametrize(
    'limit',
    [100, 1000, 10000]
)
async def test_insert_bookmarks(mongo_db, users_list, movies_list, limit):
    # Fill bookmarks collection
    users_with_bookmarks = random.choices(users_list, k=limit)
    result = await mongo_db['bookmarks'].insert_many(
        [
            {
                'user_id': user,
                'wish_list': random.choices(
                    movies_list,
                    k=random.randrange(3, 10)
                )
            } for user in users_with_bookmarks
        ]
    )

    assert len(result.inserted_ids) == limit


@pytest.mark.parametrize(
    'top_limit',
    [10, 100, 1000]
)
async def test_top_movies(mongo_db, top_limit):
    cursor = mongo_db['likes'].aggregate([
        {"$match": {"rating": {"$gte": 5}, "movie_id": {"$exists": "true"}}},
        {"$group": {"_id": "$movie_id", "rate_count": {"$sum": 1}}},
        {"$sort": {"rate_count": -1}}
    ])
    documents = await cursor.to_list(length=top_limit)

    assert len(documents) == top_limit


async def test_film_ratings(mongo_db, get_random_movie_id):
    cursor = mongo_db['likes'].aggregate([
        {"$match": {"movie_id": get_random_movie_id}},
        {
            "$project": {
                "movie_id": "$movie_id",
                "rating": "$rating",
                "dislikes": {
                    "$cond": [{"$lt": ["$rating", 5]}, 1, 0]
                },
                "likes": {
                    "$cond": [{"$gte": ["$rating", 5]}, 1, 0]
                }
            }
        },
        {
            "$group": {
                "_id": "$movie_id",
                "likes_count": {"$sum": "$likes"},
                "dislikes_count": {"$sum": "$dislikes"},
                "avg_rating": {"$avg": "$rating"},
                "rate_count": {"$sum": 1}
            }
        }
    ])
    document = await cursor.to_list(length=1)
    assert len(document) == 1
    assert isinstance(document[0], dict)
    assert set(
        [
            'likes_count',
            'dislikes_count',
            'avg_rating',
            'rate_count'
        ]
    ).issubset(document[0])


async def test_user_bookmarks(mongo_db, get_random_user_id):
    document = await mongo_db['bookmarks'].find_one(
        {"user_id": get_random_user_id}
    )
    assert isinstance(document, dict)
    assert set(['user_id', 'wish_list']).issubset(document)
