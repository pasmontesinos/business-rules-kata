from __future__ import annotations

from typing import Optional

from business_rules.domain.context_resolver.ride_attraction_context_resolver import (
    RideAttractionContextResolver,
)
from business_rules.domain.person import Person
from business_rules.domain.weather import Weather
from business_rules.domain.attraction_occupancy import AttractionOccupancy
from business_rules.domain.attraction import Attraction
from business_rules.domain.park_status import ParkStatus
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder
from business_rules.application.queries.find_person import (
    FindPersonQuery,
)
from business_rules.application.queries.find_current_weather import (
    FindCurrentWeatherQuery,
)
from business_rules.application.queries.find_current_attraction_occupancy import (
    FindCurrentAttractionOccupancyQuery,
)
from business_rules.application.queries.find_attraction import (
    FindAttractionQuery,
)
from business_rules.application.queries.find_current_park_status import (
    FindCurrentParkStatusQuery,
)


class LazyRideAttractionContextResolver(RideAttractionContextResolver):
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics

        self._person_id: Optional[str] = None
        self._attraction_id: Optional[str] = None

        self._person: Optional[Person] = None
        self._weather: Optional[Weather] = None
        self._occupancy: Optional[AttractionOccupancy] = None
        self._attraction: Optional[Attraction] = None
        self._park_status: Optional[ParkStatus] = None

    def bind(self, person_id: str, attraction_id: str) -> None:
        self._person = None
        self._weather = None
        self._occupancy = None
        self._attraction = None
        self._park_status = None
        self._person_id = person_id
        self._attraction_id = attraction_id

    @property
    def person(self) -> Person:
        if self._person:
            return self._person

        self._ensure_bound()
        assert self._person_id is not None

        self._metrics.query("FindPerson")
        self._person = self._query_bus.ask(FindPersonQuery(person_id=self._person_id))

        assert self._person is not None
        return self._person

    @property
    def weather(self) -> Weather:
        if self._weather:
            return self._weather

        self._ensure_bound()
        assert self._attraction_id is not None

        self._metrics.query("FindCurrentWeather")
        self._weather = self._query_bus.ask(
            FindCurrentWeatherQuery(attraction_id=self._attraction_id)
        )

        assert self._weather is not None
        return self._weather

    @property
    def occupancy(self) -> AttractionOccupancy:
        if self._occupancy:
            return self._occupancy

        self._ensure_bound()
        assert self._attraction_id is not None

        self._metrics.query("FindCurrentAttractionOccupancy")
        self._occupancy = self._query_bus.ask(
            FindCurrentAttractionOccupancyQuery(attraction_id=self._attraction_id)
        )

        assert self._occupancy is not None
        return self._occupancy

    @property
    def attraction(self) -> Attraction:
        if self._attraction:
            return self._attraction

        self._ensure_bound()
        assert self._attraction_id is not None

        self._metrics.query("FindAttraction")
        self._attraction = self._query_bus.ask(
            FindAttractionQuery(attraction_id=self._attraction_id)
        )

        assert self._attraction is not None
        return self._attraction

    @property
    def park_status(self) -> ParkStatus:
        if self._park_status:
            return self._park_status

        self._ensure_bound()
        self._metrics.query("FindCurrentParkStatus")
        self._park_status = self._query_bus.ask(FindCurrentParkStatusQuery())

        assert self._park_status is not None
        return self._park_status

    def _ensure_bound(self):
        if self._person_id is None or self._attraction_id is None:
            raise RuntimeError("Context resolver not bound to person and attraction")
