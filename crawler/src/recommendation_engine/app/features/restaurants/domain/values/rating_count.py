from dataclasses import dataclass


@dataclass
class RatingCount:
    count: int | None = None
    is_exceed_count: bool = False
