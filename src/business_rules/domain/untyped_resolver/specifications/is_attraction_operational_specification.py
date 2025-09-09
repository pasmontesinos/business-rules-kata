from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.attraction import Attraction

from business_rules.domain.untyped_resolver.specifications.untyped_resolver_specification import (
    UntypedResolverSpecification,
)
from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsAttractionOperationalSpecification(UntypedResolverSpecification):
    def check(self, resolver: UntypedResolver) -> SpecificationResult:
        attraction: Attraction = resolver.resolve("attraction")
        if attraction.is_under_maintenance:
            return SpecificationResult(False, "Under maintenance, please wait")

        return SpecificationResult(True, "")
