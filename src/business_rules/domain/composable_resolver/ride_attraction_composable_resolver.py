from __future__ import annotations

from abc import abstractmethod

from business_rules.domain.composable_resolver.attraction_resolver import (
    AttractionResolver,
)
from business_rules.domain.composable_resolver.occupancy_resolver import (
    OccupancyResolver,
)
from business_rules.domain.composable_resolver.park_status_resolver import (
    ParkStatusResolver,
)
from business_rules.domain.composable_resolver.person_resolver import PersonResolver
from business_rules.domain.composable_resolver.specifications.requires_fast_pass_during_peak_for_popular_specification import (
    PersonAttractionParkStatusResolver,
)
from business_rules.domain.composable_resolver.weather_resolver import WeatherResolver


class RideAttractionComposableResolver(
    PersonAttractionParkStatusResolver,
    PersonResolver,
    AttractionResolver,
    WeatherResolver,
    OccupancyResolver,
    ParkStatusResolver,
):
    @abstractmethod
    def bind(self, person_id: str, attraction_id: str) -> None: ...
