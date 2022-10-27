from pydantic import BaseSettings


class ModelsSettings(BaseSettings):
    ranking_path: str = "./models/ranking"
    retrieval_path: str = "./models/retrieval"

    class Config:
        env_prefix = "models_"


class AppSettings(BaseSettings):
    debug: bool = False
    port: int = 50051

    class Config:
        env_prefix = "app_"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    models: ModelsSettings = ModelsSettings()


settings = Settings()

if settings.app.debug:
    from devtools import debug

    debug(settings)
