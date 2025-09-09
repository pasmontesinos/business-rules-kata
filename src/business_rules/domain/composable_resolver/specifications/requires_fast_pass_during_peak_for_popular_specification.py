from __future__ import annotations

from abc import ABC

from business_rules.domain.composable_resolver.attraction_resolver import (
    AttractionResolver,
)
from business_rules.domain.composable_resolver.park_status_resolver import (
    ParkStatusResolver,
)
from business_rules.domain.composable_resolver.person_resolver import PersonResolver

from business_rules.domain.composable_resolver.specifications.specification import (
    Specification,
)

from shared.domain.specification_result import SpecificationResult


class PersonAttractionParkStatusResolver(
    PersonResolver, AttractionResolver, ParkStatusResolver, ABC
): ...


class RequiresFastPassDuringPeakForPopularSpecification(
    Specification[PersonAttractionParkStatusResolver]
):
    def check(
        self, resolver: PersonAttractionParkStatusResolver
    ) -> SpecificationResult:
        if (
            resolver.park_status.peak_hours
            and resolver.attraction.is_popular
            and not resolver.person.has_fast_pass
        ):
            return SpecificationResult(
                satisfied=False,
                reason="Fast pass required during peak hours for popular attractions",
            )
        return SpecificationResult(satisfied=True, reason="")
