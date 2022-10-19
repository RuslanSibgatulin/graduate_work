import json
from typing import List, NamedTuple, Union

from kafka import KafkaConsumer

from .backoff import backoff


class Consumer:
    def __init__(self, topic: str, server: str) -> None:
        self.server = server
        self.topic = topic
        self.connect()

    @backoff("Consumer.connect")
    def connect(self):
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=[self.server],
            auto_offset_reset="earliest",
            group_id="echo-messages-to-stdout",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            key_deserializer=lambda k: k.decode("utf-8"),
        )

    def messages(self, limit: int, timeout: int = 1000) -> Union[List, None]:
        msg: List[NamedTuple] = []
        while len(msg) < limit:
            records = self.consumer.poll(
                timeout_ms=timeout,
                max_records=limit,
            )
            for msg_list in records.values():
                msg += msg_list

        return msg or None
