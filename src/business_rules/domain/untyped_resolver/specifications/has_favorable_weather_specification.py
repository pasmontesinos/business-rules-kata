from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.untyped_resolver.specifications.untyped_resolver_specification import (
    UntypedResolverSpecification,
)
from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver
from business_rules.domain.weather import Weather
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasFavorableWeatherSpecification(UntypedResolverSpecification):
    def check(self, resolver: UntypedResolver) -> SpecificationResult:
        weather: Weather = resolver.resolve("weather")
        if weather.is_adverse:
            return SpecificationResult(False, "Adverse weather")

        return SpecificationResult(True, "")
