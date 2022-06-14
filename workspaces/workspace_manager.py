import json
import logging
import threading
import traceback

from confluent_kafka import Consumer, Producer

from messages.consts import KafkaConfig, MessageName
from messages.message_builder import MessageBuilder
from messages.message_publisher import KafkaMessagePublisher, MessagePublisher
from workspaces.models import Workspace
from workspaces.serializers import DefaultWorkspaceSerializer, WorkspaceSerializer


class WorkspaceManager:
    def __init__(self, kafka_config: dict) -> None:
        self._logger = logging.getLogger()
        self._kafka_config = kafka_config
        self._logger.debug(f"Kafka config: {json.dumps(kafka_config)}")
        self._is_subscribed = False

    def _build_publisher(self) -> MessagePublisher:
        producer_config = self._kafka_config[KafkaConfig.PRODUCER]
        producer = Producer(producer_config)
        topic = self._kafka_config[KafkaConfig.TOPICS][KafkaConfig.WORKSPACES_KEY][KafkaConfig.OUT]

        self._logger.debug(f"Build publisher with config: {json.dumps(producer_config)}")

        return KafkaMessagePublisher(producer, topic)

    def _build_message(self, message_name: str, workspace: Workspace) -> dict:
        serializer = WorkspaceSerializer(instance=workspace)
        message_builder = MessageBuilder(message_name)

        self._logger.debug(f"Workspace: {json.dumps(serializer.data)}")
        return message_builder.build(message_data=serializer.data)

    def _create_consumer(self):
        consumer_config = self._kafka_config[KafkaConfig.CONSUMER]
        consumer = Consumer(consumer_config)
        consumer.subscribe([self._kafka_config[KafkaConfig.TOPICS][KafkaConfig.WORKSPACES_KEY][KafkaConfig.IN]])

        while True:
            try:
                raw_message = consumer.poll(self._kafka_config[KafkaConfig.POLL_TIMEOUT])

                if raw_message:
                    self._logger.debug(raw_message.value())
                    consumer.commit(raw_message, asynchronous=False)
                    message = json.loads(raw_message.value())
                    message_name = message["messageName"]

                    if message_name == MessageName.DELETE_WORKSPACE:
                        payload = message["payload"]
                        Workspace.objects.filter(id=payload["id"]).delete()
                    else:
                        payload = message["payload"]
                        workspace = Workspace.objects.get(id=payload["id"])
                        serializer = DefaultWorkspaceSerializer(workspace, data=payload, partial=True)

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            self._logger.error(serializer.errors)
            except Exception as e:
                self._logger.error(e)
                self._logger.error(traceback.format_exc())

    def subscribe(self):
        self._listener = threading.Thread(target=self._create_consumer)
        self._listener.start()
        return self._is_subscribed

    def is_subscribed(self) -> bool:
        return self._is_subscribed

    def create(self, workspace: Workspace) -> None:
        self._logger.debug(f"Create workspace: {workspace.id}")
        publisher = self._build_publisher()

        message = self._build_message(MessageName.CREATE_WORKSPACE, workspace)
        self._logger.debug(f"Publish message: {json.dumps(message)}")
        publisher.publish(message)

    def delete(self, workspace: Workspace) -> None:
        self._logger.debug(f"Delete workspace: {workspace.id}")
        publisher = self._build_publisher()

        message = self._build_message(MessageName.DELETE_WORKSPACE, workspace)
        self._logger.debug(f"Publish message: {json.dumps(message)}")
        publisher.publish(message)

    def start(self, workspace: Workspace) -> None:
        self._logger.debug(f"Start workspace: {workspace.id}")
        publisher = self._build_publisher()

        message = self._build_message(MessageName.START_WORKSPACE, workspace)
        self._logger.debug(f"Publish message: {json.dumps(message)}")
        publisher.publish(message)

    def stop(self, workspace: Workspace) -> None:
        self._logger.debug(f"Start workspace: {workspace.id}")
        publisher = self._build_publisher()

        message = self._build_message(MessageName.STOP_WORKSPACE, workspace)
        self._logger.debug(f"Publish message: {json.dumps(message)}")
        publisher.publish(message)
