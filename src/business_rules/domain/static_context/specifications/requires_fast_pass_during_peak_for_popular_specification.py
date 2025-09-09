from __future__ import annotations

from business_rules.domain.static_context.ride_attraction_static_context import (
    RideAttractionStaticContext,
)
from business_rules.domain.static_context.specifications.ride_attraction_static_context_specification import (
    RideAttractionStaticContextSpecification,
)
from shared.domain.specification_result import SpecificationResult


class RequiresFastPassDuringPeakForPopularSpecification(
    RideAttractionStaticContextSpecification
):
    def check(self, context: RideAttractionStaticContext) -> SpecificationResult:
        if (
            context.park_status.peak_hours
            and context.attraction.is_popular
            and not context.person.has_fast_pass
        ):
            return SpecificationResult(
                satisfied=False,
                reason="Fast pass required during peak hours for popular attractions",
            )
        return SpecificationResult(satisfied=True, reason="")
