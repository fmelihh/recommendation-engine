from abc import ABC, abstractmethod

from ...base_entity import BaseEntity
from ...base_processor import BaseProcessor


class Restaurant(ABC, BaseEntity, BaseProcessor):
    HEADERS: dict | NotImplementedError = NotImplementedError()

    def __init__(self) -> None:
        super().__init__()



