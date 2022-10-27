import random

import pytest
from faker import Faker
from psycopg2.extras import RealDictCursor, execute_batch


def gen_scores(postgres_connection, films, users):
    fake = Faker()
    table_fields = ["user_id", "film_id", "score", "created"]
    scores_pool = [None, 5, 6, 7, 8, 9, 10]
    count = 100
    data = [
        (
            user,
            random.choice(films),
            random.choice(scores_pool),
            fake.date_time_this_year()
        ) for user in random.choices(users, k=count)
    ]
    with postgres_connection.cursor() as cur:
        fields = ", ".join(table_fields)
        values = ("%s, " * len(table_fields))[:-2]
        query = """INSERT INTO film_scores ({0}) VALUES ({1})
        ON CONFLICT ON CONSTRAINT pk_user_film DO NOTHING;
        """.format(fields, values)
        execute_batch(cur, query, data)
        postgres_connection.commit()

    return count


@pytest.mark.parametrize(
    'size', [10_000, 100_000, 1_000_000]
)
def test_insert_profiles(postgres_connection, movies_ids, users, size):
    n = 0
    while n < size:
        n += gen_scores(postgres_connection, movies_ids, users)

    print(f"Inserted {n} users")
    assert n == size


@pytest.mark.parametrize(
    "attempt",
    range(10)
)
def test_user_offer(postgres_connection, get_random_user_views, attempt):
    offer = """
        SELECT array_agg(film_id) as offer FROM film_scores
        WHERE user_id in (
            SELECT user_id FROM (
                SELECT user_id, (count(film_id)/{1} :: float) as similarity
                FROM film_scores
                WHERE film_id in {0}
                GROUP BY user_id
                ORDER BY similarity DESC
                LIMIT 10
            ) as similar_users
        )
        AND film_id NOT IN {0}
    """.format(tuple(get_random_user_views), len(get_random_user_views))

    with postgres_connection.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(offer)
        res = cur.fetchall()

    offers = list(map(dict, res))
    offer_movies = offers[0]["offer"] if len(offers) else []
    print(offer_movies)
    assert len(offers) == 1
    assert not (set(get_random_user_views) & set(offer_movies))
