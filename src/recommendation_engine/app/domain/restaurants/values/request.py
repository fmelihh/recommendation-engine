from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestValue:
    url: str
    template: str | None = None
    headers: dict | None = None
    method: Literal["GET", "POST"] = "POST"
    template_loc: Literal["params", "body"] = "body"

    @classmethod
    def _format_template(cls, template_params: dict) -> dict:
        return eval(cls.template.format(**template_params))

    @classmethod
    def retrieve_formatted_request(cls, template_params: dict) -> dict:
        return {
            "url": cls.url,
            "method": cls.method,
            "headers": cls.headers,
            cls.template_loc: cls._format_template(template_params),
        }
