import argparse
import importlib
import json

from agents import Agent
from confluent_kafka import Consumer, Producer
from handlers import Handler
from utils import load_yaml


class Manager:
    def __init__(self, handler_class: str, agent: str):
        self._kafka_config = load_yaml("configs/kafka.yml")
        self._handlers_config = load_yaml("configs/message_handlers.yml")
        self._agents_config = load_yaml("configs/agents.yml")
        self._agent: Agent = self._create_instance(self._agents_config[agent])
        self._handler: Handler = self._create_instance(self._handlers_config[handler_class], self._agent)

    def _subscribe(self):
        print(f"listening: {self._handler.get_consumer_topic(self._kafka_config)}")
        self._consumer = Consumer(self._kafka_config["consumer"])
        self._consumer.subscribe([self._handler.get_consumer_topic(self._kafka_config)])
        self._producer = Producer(self._kafka_config["producer"])
        while True:
            try:
                raw_message = self._consumer.poll(self._kafka_config["poll_timeout"])
                if raw_message:
                    message = json.loads(raw_message.value())
                    print(f"Read message: {raw_message.value()}")

                    self._consumer.commit(raw_message, asynchronous=False)
                    message = self._handler.handle(message)

                    self._producer.poll(0)
                    self._producer.produce(
                        self._handler.get_producer_topic(self._kafka_config), json.dumps(message, ensure_ascii=False)
                    )
                    self._producer.flush()

                    print(f"Produced message: {json.dumps(message)}")
            except Exception as e:
                print(e)

    def subscribe(self):
        self._subscribe()

    def _create_instance(self, class_name: str, *args):
        module_name, class_name = class_name.rsplit(".", 1)
        handler_cls = getattr(importlib.import_module(module_name), class_name)
        return handler_cls(*args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manager")
    parser.add_argument("--agent", nargs=1, required=True)
    parser.add_argument("--handler", nargs=1, required=True)

    args = parser.parse_args()
    agent = args.agent[0]
    handler = args.handler[0]

    manager = Manager(handler, agent)

    manager.subscribe()
