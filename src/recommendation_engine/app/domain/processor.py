import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from loguru import logger
from abc import ABC, abstractmethod
from typing import TypeVar, List, Literal
from pydantic import BaseModel, Field, AnyUrl


from .restaurants.values import RestaurantValue


T = TypeVar("T", *[RestaurantValue, List[RestaurantValue]])


class SyncCallParams(BaseModel):
    url: AnyUrl
    body: dict | None = Field(default=None)
    params: dict | None = Field(default=None)
    headers: dict | None = Field(default=None)
    method: Literal["GET", "POST"] = Field(default="POST")


class Processor(ABC):
    @abstractmethod
    def process(self) -> T:
        pass

    @retry(
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=30, max=120),
    )
    def synchronized_call(self, sync_call_params: SyncCallParams) -> dict:
        try:
            response = requests.request(
                url=sync_call_params.url,
                data=sync_call_params.body,
                params=sync_call_params.params,
                method=sync_call_params.method,
                headers=sync_call_params.headers,
            )
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            logger.exception(str(e))
