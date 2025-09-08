from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Person:
    person_id: str
    height_cm: int
    has_fast_pass: bool = False
