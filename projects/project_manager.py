import json
import logging
import threading
import traceback

from confluent_kafka import Consumer, Producer

from messages.consts import KafkaConfig, MessageName
from messages.message_builder import MessageBuilder
from messages.message_publisher import KafkaMessagePublisher, MessagePublisher
from projects.models import Project
from projects.serializers import DefaultProjectSerializer, ProjectSerializer


class ProjectManager:
    def __init__(self, kafka_config: dict) -> None:
        self._logger = logging.getLogger()
        self._kafka_config = kafka_config
        self._logger.debug(f"Kafka config: {json.dumps(kafka_config)}")
        self._is_subscribed = False

    def _build_publisher(self) -> MessagePublisher:
        producer_config = self._kafka_config[KafkaConfig.PRODUCER]
        producer = Producer(producer_config)
        topic = self._kafka_config[KafkaConfig.TOPICS][KafkaConfig.PROJECTS_KEY][KafkaConfig.OUT]

        self._logger.debug(f"Build publisher with config: {json.dumps(producer_config)}")

        return KafkaMessagePublisher(producer, topic)

    def _build_message(self, message_name: str, project: Project) -> dict:
        serializer = ProjectSerializer(instance=project)
        message_builder = MessageBuilder(message_name)

        self._logger.debug(f"Project: {json.dumps(serializer.data)}")
        return message_builder.build(message_data=serializer.data)

    def _create_consumer(self):
        consumer_config = self._kafka_config[KafkaConfig.CONSUMER]
        consumer = Consumer(consumer_config)
        consumer.subscribe([self._kafka_config[KafkaConfig.TOPICS][KafkaConfig.PROJECTS_KEY][KafkaConfig.IN]])

        while True:
            try:
                raw_message = consumer.poll(self._kafka_config[KafkaConfig.POLL_TIMEOUT])

                if raw_message:
                    self._logger.debug(raw_message.value())
                    consumer.commit(raw_message, asynchronous=False)
                    message = json.loads(raw_message.value())
                    message_name = message["messageName"]

                    if message_name == MessageName.DELETE_PROJECT:
                        payload = message["payload"]
                        Project.objects.filter(id=payload["id"]).delete()
                    else:
                        payload = message["payload"]
                        project = Project.objects.get(id=payload["id"])
                        serializer = DefaultProjectSerializer(project, data=payload, partial=True)

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
        self._is_subscribed = True

    def is_subscribed(self) -> bool:
        return self._is_subscribed

    def create(self, project: Project) -> None:
        self._logger.debug(f"Create project: {project.id}")
        publisher = self._build_publisher()

        message = self._build_message(MessageName.CREATE_PROJECT, project)
        self._logger.debug(f"Publish message: {json.dumps(message)}")
        publisher.publish(message)

    def delete(self, project: Project) -> None:
        self._logger.debug(f"Delete project: {project.id}")
        publisher = self._build_publisher()

        message = self._build_message(MessageName.DELETE_PROJECT, project)
        self._logger.debug(f"Publish message: {json.dumps(message)}")
        publisher.publish(message)
