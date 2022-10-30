from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    host: str = "localhost"
    port: int = 9092

    class Config:
        env_prefix = "kafka_"

    @property
    def uri(self) -> str:
        return f"{self.host}:{self.port}"


class RedisSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 6379
    db_index: int = 0

    class Config:
        env_prefix = "redis_"

    @property
    def uri(self) -> str:
        return "redis://{0}:{1}/{2}".format(
            self.host,
            self.port,
            self.db_index
        )


class MongoSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 27019
    db: str = "recom_db"

    class Config:
        env_prefix = "mongo_"

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.host}:{self.port}"


class LogstashSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5044

    class Config:
        env_prefix = "logstash_"


mongo_settings = MongoSettings()
redis_settings = RedisSettings()
logstash_settings = LogstashSettings()
kafka_settings = KafkaSettings()
