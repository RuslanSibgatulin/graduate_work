import pandas as pd
import sqlite3
from models.models import Movie


def get_sqlite_dataframe(dbfile: str) -> pd.DataFrame:
    with sqlite3.connect(dbfile) as con:
        df = pd.read_sql_query(
            """SELECT id, poster_uri FROM film_work
            WHERE poster_uri LIKE 'http%'""",
            con,
            index_col="id"
        )
        return df


def get_movies_dataframe(source: list[dict], index_col: str = None) -> pd.DataFrame:
    df_movies = pd.DataFrame.from_dict(source)
    if index_col:
        return df_movies.set_index(index_col)

    return df_movies


def get_posters(source: list[dict]) -> list[dict]:
    if not any(source):
        return []
    df = get_movies_dataframe(source, "uuid")
    return df.join(posters).to_dict('records')


db = "/home/ruslan/Документы/Practicum/Final/frontend/app/data/db_img.sqlite"
posters = get_sqlite_dataframe(db)

if __name__ == "__main__":
    movies = get_posters(
        [
            {
                "uuid": "1d2d44a5-cd27-4e88-b444-ce9927e3b596",
                "title": "Toy Story",
                "imdb_rating": 7.48
            },
            {
                "uuid": "e54983c5-9d17-4c09-a8ee-ae4ff18a01be",
                "title": "Cutthroat Island",
                "imdb_rating": 2.73
            },
            {
                "uuid": "05e75102-f062-4c3f-9f27-e76991b8800b",
                "title": "Jumanji",
                "imdb_rating": 9.15
            }
        ]
    )

    print(movies)
