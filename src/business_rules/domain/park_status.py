from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParkStatus:
    peak_hours: bool = False
