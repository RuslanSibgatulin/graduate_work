from dataclasses import dataclass
from typing import Optional


@dataclass
class Movie:
    __slots__ = ("id", "timestamp", "score")

    id: str
    timestamp: float
    score: Optional[float]
