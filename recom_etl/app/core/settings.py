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


class LogstashSettings(BaseSettings):
    LOGSTASH_HOST: str = "localhost"
    LOGSTASH_PORT: int = 5044


redis_settings = RedisSettings()
logstash_settings = LogstashSettings()
kafka_settings = KafkaSettings()
