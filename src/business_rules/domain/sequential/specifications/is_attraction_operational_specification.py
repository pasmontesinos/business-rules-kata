from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.attraction import Attraction
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsAttractionOperationalSpecification:
    def check(self, attraction: Attraction) -> SpecificationResult:
        if attraction.is_under_maintenance:
            return SpecificationResult(False, "Under maintenance, please wait")

        return SpecificationResult(True, "")
