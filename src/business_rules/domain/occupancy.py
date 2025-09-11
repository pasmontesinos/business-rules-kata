from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Occupancy:
    current_occupancy: int
    capacity: int
