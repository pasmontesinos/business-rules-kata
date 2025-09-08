from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class SpecificationResult:
    satisfied: bool
    reason: str
