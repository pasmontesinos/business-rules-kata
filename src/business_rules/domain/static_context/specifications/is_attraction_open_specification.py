from __future__ import annotations

from dataclasses import dataclass

from business_rules.domain.static_context.ride_attraction_static_context import (
    RideAttractionStaticContext,
)
from business_rules.domain.static_context.specifications.ride_attraction_static_context_specification import (
    RideAttractionStaticContextSpecification,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsAttractionOpenSpecification(RideAttractionStaticContextSpecification):
    def check(self, context: RideAttractionStaticContext) -> SpecificationResult:
        if context.attraction.closed:
            return SpecificationResult(False, "Attraction closed")

        return SpecificationResult(True, "")
