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
class IsTallEnoughSpecification(RideAttractionStaticContextSpecification):
    MIN_HEIGHT_CM = 120

    def check(self, context: RideAttractionStaticContext) -> SpecificationResult:
        if context.person.height_cm < self.MIN_HEIGHT_CM:
            return SpecificationResult(False, "Person height below minimum")

        return SpecificationResult(True, "")
