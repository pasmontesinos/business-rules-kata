from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.composable_resolver.occupancy_resolver import (
    OccupancyResolver,
)
from business_rules.domain.composable_resolver.specifications.specification import (
    Specification,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasCapacityAvailableSpecification(Specification[OccupancyResolver]):
    def check(self, resolver: OccupancyResolver) -> SpecificationResult:
        if resolver.occupancy.current_occupancy >= resolver.occupancy.capacity:
            return SpecificationResult(False, "Full capacity")

        return SpecificationResult(True, "")
