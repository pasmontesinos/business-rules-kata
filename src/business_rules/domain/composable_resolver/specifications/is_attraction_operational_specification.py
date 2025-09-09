from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.composable_resolver.attraction_resolver import (
    AttractionResolver,
)
from business_rules.domain.composable_resolver.specifications.specification import (
    Specification,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsAttractionOperationalSpecification(Specification[AttractionResolver]):
    def check(self, resolver: AttractionResolver) -> SpecificationResult:
        if resolver.attraction.is_under_maintenance:
            return SpecificationResult(False, "Under maintenance, please wait")

        return SpecificationResult(True, "")
