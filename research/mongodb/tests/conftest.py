import asyncio
from uuid import uuid4

import pandas
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient


@pytest_asyncio.fixture(scope="function")
def users_list():
    return [str(uuid4()) for _ in range(100000)]


@pytest_asyncio.fixture(scope="session")
def pandas_movies():
    return pandas.read_csv("../data/movies.csv", index_col="movieId")


@pytest_asyncio.fixture(scope="function")
def movies_by_genre(pandas_movies, genre):
    filtred = list(
        pandas_movies[pandas_movies["genres"].str.contains(genre)].index
    )
    return filtred


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def mongo_db():
    client = AsyncIOMotorClient('localhost', 27019)
    db = client['UGC_data']
    yield db


@pytest_asyncio.fixture(scope="function")
async def get_random_user_views(mongo_db):
    cursor = mongo_db['views'].aggregate(
        [
            {"$sample": {"size": 1}}
        ]
    )
    document = await cursor.to_list(length=1)
    return document[0]["viewed"]


@pytest_asyncio.fixture(scope="session")
async def get_random_movie_id(mongo_db):
    cursor = mongo_db['likes'].aggregate(
        [
            {"$match": {"movie_id": {"$exists": "true"}}},
            {"$sample": {"size": 1}}
        ]
    )
    document = await cursor.to_list(length=1)
    return document[0]["movie_id"]


@pytest_asyncio.fixture(scope="session")
async def get_users_views_count(mongo_db):
    return await mongo_db['views'].count_documents({})
