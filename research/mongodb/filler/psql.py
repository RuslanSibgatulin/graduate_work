import psycopg2
from config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_HOST, POSTGRES_USER


settings = {
    'dbname': POSTGRES_DB,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'host': POSTGRES_HOST,
    'port': POSTGRES_PORT
}


QUERY_FW = """
    SELECT
        fw.id AS id,
        array_agg(g.name) AS genres
    FROM content.film_work fw
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    GROUP BY fw.id;
"""

QUERY_GENRES = """
    SELECT name
    FROM content.genre;
"""


def get_data_by_query(query: str) -> list[dict[str, str]]:
    connection = psycopg2.connect(**settings)
    cursor = connection.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in data]
    return result


def get_filmwork_data() -> list[dict[str, str]]:
    return get_data_by_query(QUERY_FW)


def get_genres() -> list[str]:
    data = get_data_by_query(QUERY_GENRES)
    ganres_list = [genre["name"] for genre in data]
    return ganres_list


def get_genres_map(genres: list[str]) -> dict[str, list[str]]:
    genre_movies_map = {}
    for genre in genres:
        genre_movies_map[genre] = []
    movies = get_filmwork_data()
    for movie_info in movies:
        id_ = movie_info["id"]
        genres = movie_info["genres"]
        for genre in genres:
            genre_movies_map[genre].append(id_)
    return genre_movies_map
