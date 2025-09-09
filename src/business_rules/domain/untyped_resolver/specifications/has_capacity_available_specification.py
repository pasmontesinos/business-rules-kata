from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.attraction_occupancy import AttractionOccupancy
from business_rules.domain.untyped_resolver.specifications.untyped_resolver_specification import (
    UntypedResolverSpecification,
)
from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasCapacityAvailableSpecification(UntypedResolverSpecification):
    def check(self, resolver: UntypedResolver) -> SpecificationResult:
        occupancy: AttractionOccupancy = resolver.resolve("occupancy")
        if occupancy.current_occupancy >= occupancy.capacity:
            return SpecificationResult(False, "Attraction at full capacity")

        return SpecificationResult(True, "")
