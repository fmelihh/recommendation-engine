import uuid
from enum import Enum
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, model_validator


class KafkaPostfix(Enum):
    DEAD_LETTER_QUEUE = "dlq"


class KafkaTopic(Enum):
    SEARCH_RECORD = "search-record"


class KafkaHeader(BaseModel):
    exception_reason: str | None = Field(default=None)
    request_uuid: str = Field(default=str(uuid.uuid4()))
    dlq_is_enabled: Literal["true", "false"] = Field(default="false")
    dlq_options: Optional["KafkaDeadLetterQueueOptions"] = Field(default=None)

    @classmethod
    def retrieve_object_from_kafka_format(cls, data: dict[str, Any]) -> "KafkaHeader":
        if data["dlq_is_enabled"] == "true":
            return cls(
                exception_reason=data.get("exception_reason"),
                request_uuid=data["request_uuid"],
                dlq_is_enabled=data["dlq_is_enabled"],
                dlq_options=KafkaDeadLetterQueueOptions(
                    dlq_retry=data["dlq_retry"], dlq_max_retry=data["dlq_max_retry"]
                ),
            )
        else:
            return cls(**data)

    @model_validator(mode="after")
    def validate_kafka_header(self) -> "KafkaHeader":
        if self.dlq_is_enabled == "true" and self.dlq_options is None:
            raise ValueError(
                "When dead letter queue is enabled, you must specify dead letter queue options."
            )
        return self

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        data = super().model_dump(*args, **kwargs)
        if self.dlq_is_enabled == "true":
            dlq_options = data.pop("dlq_options")
            data.update(dlq_options)

        return data


class KafkaDeadLetterQueueOptions(BaseModel):
    dlq_retry: str = Field(default="0")
    dlq_max_retry: str = Field(default="10")

    def increase_dlq_retry(self):
        self.dlq_retry = str(int(self.dlq_retry) + 1)

    def is_reach_dlq_retry_to_maximum(self) -> bool:
        dlq_retry = int(self.dlq_retry)
        dlq_max_retry = int(self.dlq_max_retry)
        if dlq_retry >= dlq_max_retry:
            return True
        return False
