import json
import datetime
from typing import Any
from loguru import logger
from confluent_kafka import Producer
from fastapi.exceptions import HTTPException

from .base import AbstractKafka
from ..config import ProducerConfig
from ....usecase.commands.kafka import KafkaHeader


class KafkaProducer(AbstractKafka):
    def __init__(self):
        super(KafkaProducer, self).__init__(configuration=ProducerConfig())

    @property
    def client(self) -> Producer:
        if self._client is None:
            self._client = Producer(self.configuration.retrieve_config_dictionary())
        return self._client

    @staticmethod
    def delivery_report(err, msg):
        if err is not None:
            raise HTTPException(
                status_code=500, detail=f"message delivery failed {str(err)}"
            )

        logger.info(f"message delivered to {msg.topic()} [{msg.partition()}]")

    def produce(
        self,
        topic_name: str,
        data: list[dict[str, Any]],
        headers: KafkaHeader | list[KafkaHeader],
    ):
        if isinstance(headers, list) and len(headers) != len(data):
            raise ValueError(
                "if kafka headers are set as a list, they must be same length as the data."
            )

        list_of_headers = (
            [header.model_dump() for header in headers]
            if isinstance(headers, list)
            else [headers.model_dump()] * len(data)
        )
        timestamp = int(datetime.datetime.now().timestamp())

        for idx, produce_parameters in enumerate(zip(data, list_of_headers)):
            record, headers = produce_parameters
            self.client.produce(
                topic_name,
                value=json.dumps(record),
                key=f"{idx}_{timestamp}",
                callback=self.delivery_report,
                headers=headers,
            )

        self.client.poll(0)
        self.client.flush()
