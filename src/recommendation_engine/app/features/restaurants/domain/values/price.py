from dataclasses import dataclass


@dataclass
class Price:
    amount: float
    currency: str
