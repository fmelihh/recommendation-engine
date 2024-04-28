import json

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from loguru import logger
from abc import ABC, abstractmethod
from pydantic import field_validator
from typing import TypeVar, List, Literal
from pydantic import BaseModel, Field, AnyUrl


from .restaurants.values import RestaurantValue


T = TypeVar("T", *[RestaurantValue, List[RestaurantValue]])


class SyncCallParams(BaseModel):
    url: AnyUrl
    body: dict | str | None = Field(default=None)
    params: dict | None = Field(default=None)
    headers: dict | None = Field(default=None)
    method: Literal["GET", "POST"] = Field(default="POST")

    @field_validator("body")
    @classmethod
    def validate_body(cls, v: dict | str | None) -> dict | str | None:
        if isinstance(v, dict):
            v = json.dumps(v)
        return v


class Processor(ABC):
    @abstractmethod
    def process(self, process_limit: int | None = None) -> T:
        pass

    @staticmethod
    def _retrieve_json_from_response(response: requests.Response) -> dict | None:
        try:
            return response.json()
        except Exception as e:
            logger.exception(
                f"given response object cannot be jsonable. url: {response.url}. error details: {e}"
            )

    @retry(
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=30, max=120),
    )
    def synchronized_call(self, sync_call_params: SyncCallParams) -> requests.Response:
        try:
            response = requests.request(
                url=sync_call_params.url,
                data=sync_call_params.body,
                params=sync_call_params.params,
                method=sync_call_params.method,
                headers=sync_call_params.headers,
            )
            response.raise_for_status()
            logger.info(
                f"Sync call method was successfully completed. Requested url is: {sync_call_params.url}"
            )
            return response
        except Exception as e:
            logger.exception(str(e))
