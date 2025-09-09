from __future__ import annotations

from business_rules.domain.attraction import Attraction
from business_rules.domain.park_status import ParkStatus
from business_rules.domain.person import Person
from shared.domain.specification_result import SpecificationResult


class RequiresFastPassDuringPeakForPopularSpecification:
    def check(
        self, park_status: ParkStatus, attraction: Attraction, person: Person
    ) -> SpecificationResult:
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
