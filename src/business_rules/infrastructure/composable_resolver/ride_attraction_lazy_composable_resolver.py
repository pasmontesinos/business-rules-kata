from __future__ import annotations

from business_rules.domain.composable_resolver.ride_attraction_composable_resolver import (
    RideAttractionComposableResolver,
)
from business_rules.domain.person import Person
from business_rules.domain.weather import Weather
from business_rules.domain.attraction_occupancy import AttractionOccupancy
from business_rules.domain.attraction import Attraction
from business_rules.domain.park_status import ParkStatus
from business_rules.infrastructure.composable_resolver.query_attraction_resolver import (
    QueryAttractionResolver,
)
from business_rules.infrastructure.composable_resolver.query_occupancy_resolver import (
    QueryOccupancyResolver,
)
from business_rules.infrastructure.composable_resolver.query_park_status_resolver import (
    QueryParkStatusResolver,
)
from business_rules.infrastructure.composable_resolver.query_person_resolver import (
    QueryPersonResolver,
)
from business_rules.infrastructure.composable_resolver.query_weather_resolver import (
    QueryWeatherResolver,
)
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class LazyRideAttractionComposableResolver(RideAttractionComposableResolver):
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics

        self._person_resolver = QueryPersonResolver(self._query_bus, self._metrics)
        self._attraction_resolver = QueryAttractionResolver(
            self._query_bus, self._metrics
        )
        self._weather_resolver = QueryWeatherResolver(self._query_bus, self._metrics)
        self._occupancy_resolver = QueryOccupancyResolver(
            self._query_bus, self._metrics
        )
        self._park_status_resolver = QueryParkStatusResolver(
            self._query_bus, self._metrics
        )

    def bind(self, person_id: str, attraction_id: str) -> None:
        self._person_resolver.bind(person_id)
        self._attraction_resolver.bind(attraction_id)
        self._weather_resolver.bind(attraction_id)
        self._occupancy_resolver.bind(attraction_id)
        self._park_status_resolver.bind()

    @property
    def person(self) -> Person:
        return self._person_resolver.person

    @property
    def attraction(self) -> Attraction:
        return self._attraction_resolver.attraction

    @property
    def weather(self) -> Weather:
        return self._weather_resolver.weather

    @property
    def occupancy(self) -> AttractionOccupancy:
        return self._occupancy_resolver.occupancy

    @property
    def park_status(self) -> ParkStatus:
        return self._park_status_resolver.park_status
