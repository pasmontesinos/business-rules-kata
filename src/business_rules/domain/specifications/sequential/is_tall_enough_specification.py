from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.person import Person
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsTallEnoughSpecification:
    MIN_HEIGHT_CM = 120

    def check(self, person: Person) -> SpecificationResult:
        if person.height_cm < self.MIN_HEIGHT_CM:
            return SpecificationResult(False, "Person height below minimum")

        return SpecificationResult(True, "")
