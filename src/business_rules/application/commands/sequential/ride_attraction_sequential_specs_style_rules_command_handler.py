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
from business_rules.domain.exceptions.access_denied import AccessException
from business_rules.domain.park_status import ParkStatus
from business_rules.domain.person import Person
from business_rules.domain.ride_registration import RideRegistration
from business_rules.domain.ride_registration_repository import (
    RideRegistrationRepository,
)
from business_rules.domain.sequential.specifications.has_capacity_available_specification import (
    HasCapacityAvailableSpecification,
)
from business_rules.domain.sequential.specifications.has_favorable_weather_specification import (
    HasFavorableWeatherSpecification,
)
from business_rules.domain.sequential.specifications.is_attraction_open_specification import (
    IsAttractionOpenSpecification,
)
from business_rules.domain.sequential.specifications.is_attraction_operational_specification import (
    IsAttractionOperationalSpecification,
)
from business_rules.domain.sequential.specifications.is_tall_enough_specification import (
    IsTallEnoughSpecification,
)
from business_rules.domain.sequential.specifications.requires_fast_pass_during_peak_for_popular_specification import (
    RequiresFastPassDuringPeakForPopularSpecification,
)
from business_rules.domain.weather import Weather
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder
from shared.domain.specification_result import SpecificationResult


class RideAttractionSequentialSpecsStyleRulesCommandHandler(
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

    def _ensure_can_ride_attraction(self, command: RideAttractionCommand) -> None:
        self._metrics.rule("IsTallEnough")
        person = self._get_person(command)
        self._satisfy_or_raise(IsTallEnoughSpecification().check(person), AccessDenied)

        self._metrics.rule("IsOpen")
        attraction = self._get_attraction(command)
        self._satisfy_or_raise(
            IsAttractionOpenSpecification().check(attraction), AccessDenied
        )

        self._metrics.rule("RequiresFastPassDuringPeakForPopular")
        park_status = self._get_park_status(command)
        self._satisfy_or_raise(
            RequiresFastPassDuringPeakForPopularSpecification().check(
                park_status, attraction, person
            ),
            AccessDenied,
        )

        self._metrics.rule("IsOperational")
        self._satisfy_or_raise(
            IsAttractionOperationalSpecification().check(attraction),
            AccessTemporarilyDenied,
        )

        self._metrics.rule("IsFavorableWeather")
        weather = self._get_weather(command)
        self._satisfy_or_raise(
            HasFavorableWeatherSpecification().check(weather), AccessTemporarilyDenied
        )

        self._metrics.rule("HasCapacityAvailable")
        occupancy = self._get_current_attraction_occupancy(command)
        self._satisfy_or_raise(
            HasCapacityAvailableSpecification().check(occupancy),
            AccessTemporarilyDenied,
        )

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

    def _get_weather(self, command: RideAttractionCommand) -> Weather:
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

    def _satisfy_or_raise(
        self, spec: SpecificationResult, exception_class: type[AccessException]
    ) -> None:
        if not spec.satisfied:
            raise exception_class(spec.reason)
