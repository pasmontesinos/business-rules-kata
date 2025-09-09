from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.composable_resolver.person_resolver import PersonResolver
from business_rules.domain.composable_resolver.specifications.specification import (
    Specification,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsTallEnoughSpecification(Specification[PersonResolver]):
    MIN_HEIGHT_CM = 120

    def check(self, resolver: PersonResolver) -> SpecificationResult:
        if resolver.person.height_cm < self.MIN_HEIGHT_CM:
            return SpecificationResult(False, "Person height below minimum")

        return SpecificationResult(True, "")
