from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.occupancy import Occupancy
from business_rules.domain.untyped_resolver.specifications.untyped_resolver_specification import (
    UntypedResolverSpecification,
)
from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasCapacityAvailableSpecification(UntypedResolverSpecification):
    def check(self, resolver: UntypedResolver) -> SpecificationResult:
        occupancy: Occupancy = resolver.resolve("occupancy")
        if occupancy.current_occupancy >= occupancy.capacity:
            return SpecificationResult(False, "Full capacity")

        return SpecificationResult(True, "")
