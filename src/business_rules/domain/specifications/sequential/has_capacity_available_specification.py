from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.attraction_occupancy import AttractionOccupancy
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasCapacityAvailableSpecification:
    def check(self, attraction_ocupancy: AttractionOccupancy) -> SpecificationResult:
        if attraction_ocupancy.current_occupancy >= attraction_ocupancy.capacity:
            return SpecificationResult(False, "Attraction at full capacity")

        return SpecificationResult(True, "")
