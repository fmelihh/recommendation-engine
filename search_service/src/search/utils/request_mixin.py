import time
import json
import random
import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from typing import Literal
from pydantic import BaseModel, AnyUrl, field_validator, Field


class SyncCallParams(BaseModel):
    url: AnyUrl
    body: dict | list | str | None = Field(default=None)
    params: dict | None = Field(default=None)
    headers: dict | None = Field(default=None)
    method: Literal["GET", "POST"] = Field(default="POST")

    @field_validator("body")
    @classmethod
    def validate_body(cls, v: dict | str | None) -> dict | str | None:
        if isinstance(v, dict) or isinstance(v, list):
            v = json.dumps(v)
        return v


class SyncRequestMixin:
    @retry(
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(Exception),
        wait=wait_exponential(multiplier=1, min=30, max=120),
    )
    def synchronized_call(self, sync_call_params: SyncCallParams) -> requests.Response:
        try:
            response = requests.request(
                url=str(sync_call_params.url),
                data=sync_call_params.body,
                params=sync_call_params.params,
                method=sync_call_params.method,
                headers=sync_call_params.headers,
            )
            response.raise_for_status()
            print(
                f"Sync call method was successfully completed. Requested url is: {sync_call_params.url}"
            )
            time.sleep(random.randint(2, 5))
            return response
        except Exception as e:
            print(str(e))
