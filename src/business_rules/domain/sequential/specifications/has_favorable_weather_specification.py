from __future__ import annotations
from dataclasses import dataclass
from business_rules.domain.weather import Weather
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class HasFavorableWeatherSpecification:
    def check(self, weather: Weather) -> SpecificationResult:
        if weather.is_adverse:
            return SpecificationResult(False, "Adverse weather")

        return SpecificationResult(True, "")
