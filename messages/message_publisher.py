import json
import logging

from confluent_kafka import Producer


class MessagePublisher:
    def publish(self, message: dict) -> None:
        pass


class KafkaMessagePublisher(MessagePublisher):
    def __init__(self, producer: Producer, topic: str) -> None:
        self._logger = logging.getLogger()
        self._producer = producer
        self._topic = topic

    def publish(self, message: dict) -> None:
        self._logger.info(f"Publishing message to topic: {self._topic}")
        self._producer.poll(0)
        try:
            self._producer.produce(self._topic, json.dumps(message, ensure_ascii=False))
            self._producer.flush()
        except Exception as e:
            self._logger.debug("ERROR", e)
