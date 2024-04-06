import uuid
from abc import ABC


class BaseEntity(ABC):
    def __init__(self) -> None:
        self.entity_id = str(uuid.uuid4())

    def __eq__(self, value: "BaseEntity") -> bool:
        if isinstance(value, type(self)):
            return self.entity_id == value.entity_id

    def __hash__(self) -> int:
        return self.entity_id
