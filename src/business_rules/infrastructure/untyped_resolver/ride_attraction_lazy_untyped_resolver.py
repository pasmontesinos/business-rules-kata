from __future__ import annotations

from typing import Any, Callable

from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver

from business_rules.infrastructure.untyped_resolver.query_attraction_resolver import (
    QueryAttractionResolver,
)
from business_rules.infrastructure.untyped_resolver.query_occupancy_resolver import (
    QueryOccupancyResolver,
)
from business_rules.infrastructure.untyped_resolver.query_park_status_resolver import (
    QueryParkStatusResolver,
)
from business_rules.infrastructure.untyped_resolver.query_person_resolver import (
    QueryPersonResolver,
)
from business_rules.infrastructure.untyped_resolver.query_weather_resolver import (
    QueryWeatherResolver,
)
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class LazyRideAttractionUntypedResolver(UntypedResolver):
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
        self._key_to_callable: dict[str, Callable] = {
            "person": lambda: self._person_resolver.person,
            "attraction": lambda: self._attraction_resolver.attraction,
            "weather": lambda: self._weather_resolver.weather,
            "occupancy": lambda: self._occupancy_resolver.occupancy,
            "park_status": lambda: self._park_status_resolver.park_status,
        }

    def bind(self, *args: Any, **kwargs: Any) -> None:
        person_id = kwargs["person_id"]
        attraction_id = kwargs["attraction_id"]

        self._person_resolver.bind(person_id)
        self._attraction_resolver.bind(attraction_id)
        self._weather_resolver.bind(attraction_id)
        self._occupancy_resolver.bind(attraction_id)
        self._park_status_resolver.bind()

    def resolve(self, key: str) -> Any:
        if key not in self._key_to_callable:
            raise KeyError(f"Key '{key}' not found in resolver.")

        return self._key_to_callable[key]()
