from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    KAFKA_HOST: str = "localhost"
    KAFKA_PORT: int = 9092

    @property
    def uri(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB_INDEX: int = 0

    @property
    def uri(self) -> str:
        return "redis://{0}:{1}/{2}".format(
            self.REDIS_HOST,
            self.REDIS_PORT,
            self.REDIS_DB_INDEX
        )


class MongoSettings(BaseSettings):
    MONGO_HOST: str = "127.0.0.1"
    MONGO_PORT: int = 27019
    MONGO_DB: str = "recommendations"

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"


class LogstashSettings(BaseSettings):
    LOGSTASH_HOST: str = "localhost"
    LOGSTASH_PORT: int = 5044


mongo_settings = MongoSettings()
redis_settings = RedisSettings()
logstash_settings = LogstashSettings()
kafka_settings = KafkaSettings()
