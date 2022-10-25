import uuid

import pandas
import pytest
from psycopg2 import connect as _pg_conn


@pytest.fixture(scope="session")
def pandas_movies():
    return pandas.read_csv("../data/movies.csv", index_col="movieId")


@pytest.fixture(scope="function")
def movies_ids(pandas_movies):
    return list(pandas_movies.index)


@pytest.fixture(scope="session")
def users():
    users = [str(uuid.uuid4()) for _ in range(1000000)]
    return users


@pytest.fixture(scope="session")
def postgres_connection():
    dsn = {
        "dbname": "db_test",
        "user": "test",
        "password": "123qwe",
        "host": "127.0.0.1"
    }
    with _pg_conn(**dsn) as pg_conn:
        yield pg_conn


@pytest.fixture(scope="session")
def get_random_user_views(postgres_connection):
    user_profile = """
        SELECT array_agg(film_id) as movies, count(film_id)
        FROM film_scores
        GROUP BY user_id
        HAVING count(film_id) > 3
        ORDER BY random()
        LIMIT 1;
    """

    with postgres_connection.cursor() as cur:
        cur.execute(user_profile)
        res = cur.fetchone()
        return res[0]
