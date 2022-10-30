import time
from random import choice
from uuid import uuid4

from config import GENRES, GENRES_COUNT


MOVIES_IN_HISTORY = 120
ONE_DAY = 60 * 60 * 24


def get_genres(genres: str) -> list[str]:
    genres_count = choice(GENRES_COUNT)
    genres_set = set()
    for num in range(genres_count):
        genres_set.add(choice(genres))
    return list(genres_set)


def generate_user(genres: list[str], genres_map: dict, uuid_: str = None) -> dict:
    if uuid_:
        user_id = uuid_
    else:
        user_id = str(uuid4())
    payload = {"user_id": user_id, "movies": {}}
    genres = get_genres(genres)
    size = MOVIES_IN_HISTORY // len(genres)
    time_start = int(time.time()) - (MOVIES_IN_HISTORY * ONE_DAY)
    for genre in genres:
        movies = genres_map[genre]
        for num in range(size):
            payload["movies"][choice(movies)] = {"timestamp": time_start, "score": choice(range(1, 11))}
            time_start += ONE_DAY
    return payload





