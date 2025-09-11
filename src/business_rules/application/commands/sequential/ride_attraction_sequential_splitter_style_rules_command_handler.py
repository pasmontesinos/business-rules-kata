from __future__ import annotations

from business_rules.application import RideAttractionCommandHandler
from business_rules.application.commands.ride_attraction_command import (
    RideAttractionCommand,
)
from business_rules.domain.attraction import Attraction
from business_rules.domain.occupancy import Occupancy
from business_rules.domain.exceptions import AccessDenied, AccessTemporarilyDenied
from business_rules.application.queries.find_current_attraction_occupancy import (
    FindCurrentAttractionOccupancyQuery,
)
from business_rules.application.queries.find_current_weather import (
    FindCurrentWeatherQuery,
)
from business_rules.application.queries.find_person import (
    FindPersonQuery,
)
from business_rules.application.queries.find_attraction import (
    FindAttractionQuery,
)
from business_rules.application.queries.find_current_park_status import (
    FindCurrentParkStatusQuery,
)
from business_rules.domain.park_status import ParkStatus
from business_rules.domain.person import Person
from business_rules.domain.ride_registration import RideRegistration
from business_rules.domain.ride_registration_repository import (
    RideRegistrationRepository,
)
from business_rules.domain.weather import Weather
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class RideAttractionSequentialSplitterStyleRulesCommandHandler(
    RideAttractionCommandHandler
):
    def __init__(
        self,
        repo: RideRegistrationRepository,
        query_bus: QueryBus,
        metrics: MetricsRecorder,
    ) -> None:
        self._repo = repo
        self._query_bus = query_bus
        self._metrics = metrics
        self._person: Person | None = None
        self._attraction: Attraction | None = None
        self._weather: Weather | None = None
        self._occupancy: Occupancy | None = None
        self._park_status: ParkStatus | None = None

    def handle(self, command: RideAttractionCommand) -> None:
        self._ensure_can_ride_attraction(command)

        registration = RideRegistration.create(
            person_id=command.person_id,
            attraction_id=command.attraction_id,
        )
        self._repo.save(registration)

    def _ensure_can_ride_attraction(self, command):
        if not self._is_tall_enough(command):
            raise AccessDenied("Person height below minimum")

        if not self._is_open(command):
            raise AccessDenied("Attraction closed")

        if not self._has_fast_pass_when_required(command):
            raise AccessDenied(
                "Fast pass required during peak hours for popular attractions"
            )

        if not self._is_operational(command):
            raise AccessTemporarilyDenied("Under maintenance, please wait")

        if not self._is_favorable_weather(command):
            raise AccessTemporarilyDenied("Adverse weather")

        if not self._has_capacity_available(command):
            raise AccessTemporarilyDenied("Full capacity")

    def _has_fast_pass_when_required(self, command: RideAttractionCommand) -> bool:
        self._metrics.rule("RequiresFastPassDuringPeakForPopular")
        person = self._get_person(command)
        attraction = self._get_attraction(command)
        park_status = self._get_park_status(command)

        if (
            park_status.peak_hours
            and attraction.is_popular
            and not person.has_fast_pass
        ):
            return False
        return True

    def _is_favorable_weather(self, command: RideAttractionCommand) -> bool:
        self._metrics.rule("IsFavorableWeather")
        weather = self._get_weather(command)
        return not weather.is_adverse

    def _is_tall_enough(self, command: RideAttractionCommand) -> bool:
        self._metrics.rule("IsTallEnough")
        person = self._get_person(command)
        return person.height_cm >= 120

    def _has_capacity_available(self, command: RideAttractionCommand) -> bool:
        self._metrics.rule("HasCapacityAvailable")
        occupancy = self._get_current_attraction_occupancy(command)
        return occupancy.current_occupancy < occupancy.capacity

    def _is_operational(self, command: RideAttractionCommand) -> bool:
        self._metrics.rule("IsOperational")
        attraction = self._get_attraction(command)
        return not attraction.is_under_maintenance

    def _is_open(self, command: RideAttractionCommand) -> bool:
        self._metrics.rule("IsOpen")
        attraction = self._get_attraction(command)
        return not attraction.closed

    def _get_person(self, command: RideAttractionCommand) -> Person:
        if self._person:
            return self._person

        self._metrics.query("FindPerson")
        self._person = self._query_bus.ask(FindPersonQuery(person_id=command.person_id))
        assert self._person

        return self._person

    def _get_attraction(self, command: RideAttractionCommand) -> Attraction:
        if self._attraction:
            return self._attraction

        self._metrics.query("FindAttraction")
        self._attraction = self._query_bus.ask(
            FindAttractionQuery(attraction_id=command.attraction_id)
        )
        assert self._attraction

        return self._attraction

    def _get_weather(self, command):
        if self._weather:
            return self._weather

        self._metrics.query("FindCurrentWeather")
        self._weather = self._query_bus.ask(
            FindCurrentWeatherQuery(attraction_id=command.attraction_id)
        )
        assert self._weather

        return self._weather

    def _get_current_attraction_occupancy(
        self, command: RideAttractionCommand
    ) -> Occupancy:
        if self._occupancy:
            return self._occupancy

        self._metrics.query("FindCurrentAttractionOccupancy")
        self._occupancy = self._query_bus.ask(
            FindCurrentAttractionOccupancyQuery(attraction_id=command.attraction_id)
        )
        assert self._occupancy

        return self._occupancy

    def _get_park_status(self, command: RideAttractionCommand):
        if self._park_status:
            return self._park_status

        self._metrics.query("FindCurrentParkStatus")
        self._park_status = self._query_bus.ask(FindCurrentParkStatusQuery())
        assert self._park_status

        return self._park_status
