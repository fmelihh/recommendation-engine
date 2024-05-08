from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestValue:
    url: str
    template: str | None = None
    headers: dict | None = None
    method: Literal["GET", "POST"] = "POST"
    template_loc: Literal["params", "body"] = "body"

    def _format_template(self, template_params: dict) -> dict:
        return eval(self.template.strip().format(**template_params))

    def retrieve_formatted_request(self, template_params: dict) -> dict:
        return {
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            self.template_loc: self._format_template(template_params),
        }
