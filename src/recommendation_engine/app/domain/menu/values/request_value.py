from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestValue:
    url: str
    template: str | None = None
    headers: dict | None = None
    method: Literal["GET", "POST"] = "POST"
    template_loc: Literal["params", "body"] = "body"

    def _format_template(self, template_params: dict) -> dict | None:
        if not self.template:
            return None

        return eval(self.template.strip().format(**template_params))

    def retrieve_formatted_request(self, template_params: dict) -> dict:
        formatted_req = {
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
        }
        template_param = self._format_template(template_params)
        if template_param is not None:
            formatted_req[self.template_loc] = template_param
        return formatted_req
