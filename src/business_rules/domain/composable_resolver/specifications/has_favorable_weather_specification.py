from __future__ import annotations
from dataclasses import dataclass

from business_rules.domain.composable_resolver.specifications.specification import (
    Specification,
)
from business_rules.domain.composable_resolver.weather_resolver import WeatherResolver
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasFavorableWeatherSpecification(Specification[WeatherResolver]):
    def check(self, resolver: WeatherResolver) -> SpecificationResult:
        if resolver.weather.is_adverse:
            return SpecificationResult(False, "Adverse weather")

        return SpecificationResult(True, "")
