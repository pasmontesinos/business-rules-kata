from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AttractionOccupancy:
    current_occupancy: int
    capacity: int
