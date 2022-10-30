from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: str = Field(..., alias="uuid")
    rating: float = Field(..., alias="imdb_rating")
    title: str

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class GerneMovies(BaseModel):
    genre: str
    movies: list[Movie]
