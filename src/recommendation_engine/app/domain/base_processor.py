from abc import ABC, abstractmethod


class BaseProcessor(ABC):
    @abstractmethod
    def process():
        pass
