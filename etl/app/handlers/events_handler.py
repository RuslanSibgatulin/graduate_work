import asyncio
import logging
import logging.config
from typing import Any, List, Optional

import orjson
from aiokafka import AIOKafkaConsumer, TopicPartition
from aiokafka.structs import ConsumerRecord
from db.backoff import aiobackoff
from db.redis import RedisCache

logger = logging.getLogger(__name__)


class EventsHandler:
    def __init__(
        self,
        kafka_url: str,
        redis: RedisCache,
        events_registry: dict
    ) -> None:
        self.redis = redis
        self.kafka_url = kafka_url
        self.config = events_registry
        self.prepare()

    def prepare(self) -> None:
        for topic in self.config:
            handlers_classes = self.config[topic].get("handlers", [])
            self.config[topic]["instances"] = [
                handler_class(topic) for handler_class in handlers_classes
            ]

    def get_handlers(self, topic) -> List[Any]:
        return self.config[topic]["instances"]

    def get_model(self, topic) -> Any:
        return self.config.get(topic, {}).get("model", None)

    @aiobackoff("Kafka.consume", logger)
    async def consume(self, topic: str) -> None:
        logger.info("Consume topic %s", topic)
        consumer = self.create_consumer()
        tp = TopicPartition(topic, 0)
        await consumer.start()
        consumer.assign([tp])
        try:
            await self.seek(consumer, topic, tp)
            # Consume topic messages
            async for msg in consumer:
                context = self.transform(msg)
                if not context:
                    continue
                # Exec all assigned handlers
                for handler in self.get_handlers(topic):
                    await handler.load(context)
                await self.save_offset(topic, msg)
        finally:
            await self.redis.close()
            await consumer.stop()

    def create_consumer(self) -> AIOKafkaConsumer:
        consumer = AIOKafkaConsumer(
            auto_offset_reset="earliest",
            bootstrap_servers=self.kafka_url,
            enable_auto_commit=False,
            retry_backoff_ms=500,
            max_poll_interval_ms=60000,
            metadata_max_age_ms=60000,
            value_deserializer=lambda v: orjson.loads(v.decode("utf-8")))

        return consumer

    async def save_offset(self, topic, msg):
        REDIS_HASH_KEY = f"consumer:{topic}:offset"
        return await self.redis.set(REDIS_HASH_KEY, msg.offset)

    async def seek(self, consumer, topic, tp):
        REDIS_HASH_KEY = f"consumer:{topic}:offset"
        offset = await self.redis.get(REDIS_HASH_KEY)
        if offset:
            consumer.seek(tp, offset=offset + 1)

    def transform(self, event: ConsumerRecord) -> Optional[Any]:
        obj = event.value | {"event_time": event.timestamp // 1000}
        model = self.get_model(event.topic)
        if model:
            return model.parse_obj(obj)

        logger.info("No model for topic %s", event.topic)
        return None

    def start(self):
        loop = asyncio.get_event_loop()
        tasks = (self.consume(topic) for topic in self.config)
        future = asyncio.gather(*tasks, return_exceptions=True)
        loop.run_until_complete(future)
