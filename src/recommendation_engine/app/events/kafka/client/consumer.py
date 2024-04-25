import json
from loguru import logger
from typing import Generator, Any
from confluent_kafka import Consumer
from contextlib import contextmanager

from ..config import ConsumerConfig
from .producer import KafkaProducer
from .base import AbstractKafka, KafkaClient
from ....usecase.commands.kafka import KafkaPostfix, KafkaHeader


class KafkaConsumer(AbstractKafka):
    def __init__(
        self,
        timeout: int = 600,
        batch_size: int = 1000,
        producer: KafkaProducer | None = None,
        # dlq_errors: list[BaseException] | None = None,
    ):
        self.timeout = timeout
        self._producer = producer
        self.batch_size = batch_size
        # self.dlq_errors = (
        #     dlq_errors
        #     if isinstance(dlq_errors, list) and len(dlq_errors) > 0
        #     else [Exception]
        # )
        super().__init__(configuration=ConsumerConfig())

    @property
    def producer(self) -> KafkaProducer:
        if self._producer is None:
            self._producer = KafkaProducer()
        return self._producer

    @property
    def client(self) -> KafkaClient:
        if self._client is None:
            self._client = Consumer(self.configuration.retrieve_config_dictionary())
        return self._client

    def rotate_dql_messages(
        self,
        topic_names: list[str],
        headers: list[dict[str, Any]],
        data_values: list[dict[str, Any]],
    ):
        dlq_rotate_hashmap = {}
        for topic, header, data_val in zip(topic_names, headers, data_values):
            kafka_header = KafkaHeader.retrieve_object_from_kafka_format(header)

            if not kafka_header.dlq_options.is_reach_dlq_retry_to_maximum():
                topic = topic.replace(
                    f"-{KafkaPostfix.DEAD_LETTER_QUEUE.value}", ""
                ).strip()

            if topic not in dlq_rotate_hashmap:
                dlq_rotate_hashmap[topic] = {"data": [], "headers": []}

            dlq_rotate_hashmap[topic]["data"].append(data_val)
            dlq_rotate_hashmap[topic]["headers"].append(kafka_header)

        for topic, values in dlq_rotate_hashmap.items():
            self.producer.produce(
                topic_name=topic, headers=values["headers"], data=values["data"]
            )

    @staticmethod
    def _format_consumed_data(data_list: list) -> dict[str, list[dict[str, Any]]]:
        headers = []
        topic_names = []
        data_values = []
        for data in data_list:
            headers.append(
                {
                    key: value.decode("utf-8") if isinstance(value, bytes) else value
                    for key, value in dict(data.headers()).items()
                }
            )
            topic_names.append(data.topic())
            data_values.append(json.loads(data.value().decode("utf-8")))

        return {
            "headers": headers,
            "topic_names": topic_names,
            "data_values": data_values,
        }

    def process_dead_letter_queue_logic(
        self,
        topic: str,
        exception_reason: str,
        headers: list[dict[str, Any]],
        data_values: list[dict[str, Any]],
    ):
        formatted_headers = []
        formatted_data_values = []

        for idx, header in enumerate(headers):
            kafka_header = KafkaHeader.retrieve_object_from_kafka_format(data=header)
            kafka_header.exception_reason = exception_reason

            if kafka_header.dlq_is_enabled == "false":
                continue

            kafka_header.dlq_options.increase_dlq_retry()

            formatted_headers.append(kafka_header)
            formatted_data_values.append(data_values[idx])

        self.producer.produce(
            headers=formatted_headers,
            data=formatted_data_values,
            topic_name=f"{topic}-{KafkaPostfix.DEAD_LETTER_QUEUE.value}",
        )

    @contextmanager
    def dlq_context(
        self,
        topic: str | list[str],
        headers: list[dict[str, Any]],
        data_values: list[dict[str, Any]],
    ) -> Generator:
        try:
            yield
        except Exception as e:
            logger.exception(
                f"An error occurred while processing consumed datas. error details: {e}"
            )
            self.process_dead_letter_queue_logic(
                topic=topic,
                headers=headers,
                data_values=data_values,
                exception_reason=str(e),
            )

    def consume(
        self, topic: str
    ) -> Generator[tuple[list[dict[str, Any]], list[dict[str, Any]]], None, None]:

        self.client.subscribe([topic])
        while True:
            data_list = self.client.consume(self.batch_size, timeout=self.timeout)
            if not data_list:
                break

            formatted_data_list = self._format_consumed_data(data_list)
            yield (
                formatted_data_list["topic_names"],
                formatted_data_list["headers"],
                formatted_data_list["data_values"],
            )
