from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Attraction:
    is_under_maintenance: bool
    closed: bool = False
    is_popular: bool = False
