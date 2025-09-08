from __future__ import annotations

from business_rules.application import RideAttractionCommandHandler
from business_rules.application.commands.ride_attraction_command import (
    RideAttractionCommand,
)
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
from business_rules.domain.ride_registration import RideRegistration
from business_rules.domain.ride_registration_repository import (
    RideRegistrationRepository,
)
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class RideAttractionSequentialLumperStyleRulesCommandHandler(
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

    def handle(self, command: RideAttractionCommand) -> None:
        self._ensure_can_ride_attraction(command)

        registration = RideRegistration.create(
            person_id=command.person_id,
            attraction_id=command.attraction_id,
        )
        self._repo.save(registration)

    def _ensure_can_ride_attraction(self, command: RideAttractionCommand):
        self._metrics.rule("IsTallEnough")
        self._metrics.query("FindPerson")
        person = self._query_bus.ask(FindPersonQuery(person_id=command.person_id))
        if not person.height_cm >= 120:
            raise AccessDenied("Person height below minimum")

        self._metrics.rule("IsOpen")
        self._metrics.query("FindAttraction")
        attraction = self._query_bus.ask(
            FindAttractionQuery(attraction_id=command.attraction_id)
        )
        if attraction.closed:
            raise AccessDenied("Attraction closed")

        self._metrics.rule("RequiresFastPassDuringPeakForPopular")
        self._metrics.query("FindCurrentParkStatus")
        park_status = self._query_bus.ask(FindCurrentParkStatusQuery())

        if (
            park_status.peak_hours
            and attraction.is_popular
            and not person.has_fast_pass
        ):
            raise AccessDenied(
                "Fast pass required during peak hours for popular attractions"
            )

        self._metrics.rule("IsOperational")
        if attraction.is_under_maintenance:
            raise AccessTemporarilyDenied("Under maintenance, please wait")

        self._metrics.rule("IsFavorableWeather")
        self._metrics.query("FindCurrentWeather")
        weather = self._query_bus.ask(
            FindCurrentWeatherQuery(attraction_id=command.attraction_id)
        )
        if weather.is_adverse:
            raise AccessTemporarilyDenied("Adverse weather")

        self._metrics.rule("HasCapacityAvailable")
        self._metrics.query("FindCurrentAttractionOccupancy")
        occupancy = self._query_bus.ask(
            FindCurrentAttractionOccupancyQuery(attraction_id=command.attraction_id)
        )
        if occupancy.current_occupancy == occupancy.capacity:
            raise AccessTemporarilyDenied("Attraction at full capacity")
