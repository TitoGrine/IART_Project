from dataclasses import dataclass


@dataclass
class Tweet:
    id: str
    tweet: str
    dimension: str
    intensity: int
    intensity_class: str
