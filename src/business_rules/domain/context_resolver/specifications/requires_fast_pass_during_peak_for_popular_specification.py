from __future__ import annotations

from business_rules.domain.context_resolver.ride_attraction_context_resolver import (
    RideAttractionContextResolver,
)
from business_rules.domain.context_resolver.specifications.ride_attraction_static_context_specification import (
    RideAttractionContextResolverSpecification,
)
from shared.domain.specification_result import SpecificationResult


class RequiresFastPassDuringPeakForPopularSpecification(
    RideAttractionContextResolverSpecification
):
    def check(self, context: RideAttractionContextResolver) -> SpecificationResult:
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
