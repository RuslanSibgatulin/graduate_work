from pydantic import BaseSettings


class Config(BaseSettings):
    secret_key: str = "extra secret"
    hash_algorithm: str = "SHA-256"
    mongo_host: str = "127.0.0.1"
    mongo_port: int = 27017
    mongo_db: str = "like"
    mongo_user_collection: str = "profiles"
    user_genres_check_url: str = "http://127.0.0.1/api/v1/auth/genres"
    url_movies_by_genre: str = "http://127.0.0.1/api/v1/film"
    url_movies_name: str = "http://127.0.0.1/api/v1/film/names"
    grpc_addr: str = "localhost:50051"
    logstash_host: str = "logstash"
    logstash_port: int = 5044

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.mongo_host}:{self.mongo_port}"


config = Config()
