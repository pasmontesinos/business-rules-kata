from __future__ import annotations

from business_rules.domain.attraction import Attraction

from business_rules.domain.park_status import ParkStatus
from business_rules.domain.person import Person
from business_rules.domain.untyped_resolver.specifications.untyped_resolver_specification import (
    UntypedResolverSpecification,
)
from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver

from shared.domain.specification_result import SpecificationResult


class RequiresFastPassDuringPeakForPopularSpecification(UntypedResolverSpecification):
    def check(self, resolver: UntypedResolver) -> SpecificationResult:
        person: Person = resolver.resolve("person")
        attraction: Attraction = resolver.resolve("attraction")
        park_status: ParkStatus = resolver.resolve("park_status")
        if (
            park_status.peak_hours
            and attraction.is_popular
            and not person.has_fast_pass
        ):
            return SpecificationResult(
                satisfied=False,
                reason="Fast pass required during peak hours for popular attractions",
            )
        return SpecificationResult(satisfied=True, reason="")
