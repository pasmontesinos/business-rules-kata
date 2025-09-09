from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.context_resolver.ride_attraction_context_resolver import (
    RideAttractionContextResolver,
)
from business_rules.domain.context_resolver.specifications.ride_attraction_static_context_specification import (
    RideAttractionContextResolverSpecification,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasCapacityAvailableSpecification(RideAttractionContextResolverSpecification):
    def check(self, context: RideAttractionContextResolver) -> SpecificationResult:
        if context.occupancy.current_occupancy >= context.occupancy.capacity:
            return SpecificationResult(False, "Attraction at full capacity")

        return SpecificationResult(True, "")
