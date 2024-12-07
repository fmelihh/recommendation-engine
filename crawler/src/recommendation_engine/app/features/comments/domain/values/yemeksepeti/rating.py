from dataclasses import dataclass


@dataclass(frozen=True)
class YemekSepetiRating:
    overall_rating: int | None
    restaurant_rating: int | None
    rider_rating: int | None
