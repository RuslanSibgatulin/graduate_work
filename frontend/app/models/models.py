from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    user_id: UUID
    username: str
    email: str | None = None


class Token(BaseModel):
    access_token: str
    refresh_token: str


class Movie(BaseModel):
    uuid: str
    imdb_rating: float
    title: str


class MovieLike(BaseModel):
    movie_id: str
    score: int


class MovieProgress(BaseModel):
    movie_id: str
    time: int
    total_time: int
