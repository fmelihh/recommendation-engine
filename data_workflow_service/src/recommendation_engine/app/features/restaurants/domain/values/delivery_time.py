from dataclasses import dataclass


@dataclass
class DeliveryTime:
    le: float
    ge: float
    unit: str | None = None
