from __future__ import annotations

from dataclasses import dataclass

from business_rules.domain.attraction import Attraction

from business_rules.domain.untyped_resolver.specifications.untyped_resolver_specification import (
    UntypedResolverSpecification,
)
from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class IsAttractionOpenSpecification(UntypedResolverSpecification):
    def check(self, resolver: UntypedResolver) -> SpecificationResult:
        attraction: Attraction = resolver.resolve("attraction")
        if attraction.closed:
            return SpecificationResult(False, "Attraction closed")

        return SpecificationResult(True, "")
