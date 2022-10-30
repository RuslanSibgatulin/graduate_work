from dataclasses import dataclass


@dataclass(slots=True)
class MovieContextInfo:
    movie_id: str
