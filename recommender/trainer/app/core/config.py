from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 27017
    db_name: str = "recom_db"
    profiles_collection: str = "profiles"

    class Config:
        env_prefix = "mongo_"


class MoviesApiSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 80

    class Config:
        env_prefix = "movies_api_"


class CollectSettings(BaseSettings):
    ratings_output_dir: str = "../ratings-data"
    views_output_dir: str = "../views-data"
    movies_output_dir: str = "../movies-data"

    max_views_length: int = 10

    mongo: MongoSettings = MongoSettings()
    movies_api: MoviesApiSettings = MoviesApiSettings()

    class Config:
        env_prefix = "collect_"


class TrainSettings(BaseSettings):
    movies_input_dir: str = "../movies-data"
    views_input_dir: str = "../views-data"
    retrieval_output_dir: str = "../models/retrieval"
    max_views_length: int = 10

    ratings_input_dir: str = "../ratings-data"
    ranking_output_dir: str = "../models/ranking"

    class Config:
        env_prefix = "train_"


class Settings(BaseSettings):
    collect: CollectSettings = CollectSettings()

    train: TrainSettings = TrainSettings(
        movies_input_dir=collect.movies_output_dir,
        ratings_input_dir=collect.ratings_output_dir,
        views_input_dir=collect.views_output_dir,
        max_views_length=collect.max_views_length,
    )


def get_settings() -> Settings:
    return Settings()
