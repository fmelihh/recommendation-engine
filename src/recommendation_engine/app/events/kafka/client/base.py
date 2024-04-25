from typing import TypeVar
from abc import ABC, abstractmethod
from confluent_kafka import Consumer, Producer

from ..config import AbstractKafkaConfig

KafkaClient = TypeVar("KafkaClient", Consumer, Producer)


class AbstractKafka(ABC):
    def __init__(self, configuration: AbstractKafkaConfig):
        self._client = None
        self.configuration = configuration

    @property
    @abstractmethod
    def client(self) -> KafkaClient:
        pass
