import logging

from core.config import events_config
from core.logger import LOGGING
from core.settings import kafka_settings, redis_settings
from db.redis import RedisCache
from handlers.events_handler import EventsHandler

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("Events-Handler")


if __name__ == "__main__":
    logger.info("Started")
    redis = RedisCache(redis_settings.uri)
    events = EventsHandler(kafka_settings.uri, redis, events_config)
    try:
        events.start()
    except KeyboardInterrupt:
        logger.info("Stop reading")

    logger.info("Finished")
