from __future__ import annotations

from dataclasses import dataclass

from business_rules.domain.attraction import Attraction
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsAttractionOpenSpecification:
    def check(self, attraction: Attraction) -> SpecificationResult:
        if attraction.closed:
            return SpecificationResult(False, "Attraction closed")

        return SpecificationResult(True, "")
