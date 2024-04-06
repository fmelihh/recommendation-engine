from abc import ABC, abstractmethod

from ...entity import BaseEntity
from ...processor import BaseProcessor


class Restaurants(ABC, BaseEntity, BaseProcessor):
    HEADERS: dict | NotImplementedError = NotImplementedError()

    def __init__(self) -> None:
        super().__init__()
