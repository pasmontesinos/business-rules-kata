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
class IsAttractionOpenSpecification(RideAttractionContextResolverSpecification):
    def check(self, context: RideAttractionContextResolver) -> SpecificationResult:
        if context.attraction.closed:
            return SpecificationResult(False, "Attraction closed")

        return SpecificationResult(True, "")
