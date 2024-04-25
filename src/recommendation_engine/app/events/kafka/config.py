import dataclasses
from abc import ABC, abstractmethod


class AbstractKafkaConfig(ABC):
    bootstrap_servers: str = "pkc-12576z.us-west2.gcp.confluent.cloud:9092"
    security_protocol: str = "SASL_SSL"
    sasl_mechanisms: str = "PLAIN"
    sasl_username: str = "KMF2L2K5FY5FSWD6"
    sasl_password: str = (
        "LhS2a/phg9FljZYjUCdo9yY+FalusxsqT6T73NHKyXpGyeRs9AKestL70pRy05wN"
    )

    @abstractmethod
    def retrieve_config_dictionary(self) -> dict:
        pass


@dataclasses.dataclass(frozen=True)
class ProducerConfig(AbstractKafkaConfig):
    def retrieve_config_dictionary(self) -> dict:
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "security.protocol": self.security_protocol,
            "sasl.mechanisms": self.sasl_mechanisms,
            "sasl.username": self.sasl_username,
            "sasl.password": self.sasl_password,
        }


@dataclasses.dataclass(frozen=True)
class ConsumerConfig(AbstractKafkaConfig):
    session_timeout_ms: str = "45000"
    group_id: str = "python-group-1"
    auto_offset_reset: str = "earliest"

    def retrieve_config_dictionary(self) -> dict:
        return {
            "bootstrap.servers": self.bootstrap_servers,
            "security.protocol": self.security_protocol,
            "sasl.mechanisms": self.sasl_mechanisms,
            "sasl.username": self.sasl_username,
            "sasl.password": self.sasl_password,
            "session.timeout.ms": self.session_timeout_ms,
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }
