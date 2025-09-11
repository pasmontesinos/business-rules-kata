from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.occupancy import Occupancy
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasCapacityAvailableSpecification:
    def check(self, ocupancy: Occupancy) -> SpecificationResult:
        if ocupancy.current_occupancy >= ocupancy.capacity:
            return SpecificationResult(False, "Full capacity")

        return SpecificationResult(True, "")
