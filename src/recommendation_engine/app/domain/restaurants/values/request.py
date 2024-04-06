from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestValue:
    template: str | None = None
    headers: dict | None = None
    method: Literal["GET", "POST"] = "POST"
    template_loc: Literal["parameter", "body"] = "body"

    @classmethod
    def format_template(cls, template_params: dict):
        return cls.template.format(**template_params)
