from dataclasses import dataclass


@dataclass(frozen=True)
class GeoValue:
    lat: float
    lon: float
