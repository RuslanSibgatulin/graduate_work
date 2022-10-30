from typing import List

from pydantic import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: str = "extra secret"
    HASH_ALGORITHM: str = "SHA-256"
    MONGO_HOST: str = "127.0.0.1"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "like"
    MONGO_USER_COLLECTION: str = "user"
    USER_GENRES_CHECK_URL: str = "http://127.0.0.1/auth/v1/genres"
    URL_MOVIES_BY_GENRES: str = "http://127.0.0.1/api/v1/film"
    URL_MOVIES_NAME: str = "http://127.0.0.1/api/v1/film/names"
    GRPC_ADDR: str = "localhost:50051"
    LOGSTASH_HOST: str = "logstash"
    LOGSTASH_PORT: int = 5044

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"

    def get_collections(self) -> List[str]:
        return []


config = Config()