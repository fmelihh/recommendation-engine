from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True)
class RequestValue:
    template: str | None = None
    headers: dict | None = None
    method: Literal["GET", "POST"] = "POST"
    template_loc: Literal["parameter", "body"] = "body"

    def fill_template(self, **kwargs) -> str:
        return self.template.format(**kwargs)
