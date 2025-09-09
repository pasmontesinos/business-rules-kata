from __future__ import annotations

from business_rules.application import RideAttractionCommandHandler
from business_rules.application.commands.ride_attraction_command import (
    RideAttractionCommand,
)
from business_rules.domain.attraction import Attraction
from business_rules.domain.attraction_occupancy import AttractionOccupancy
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
from business_rules.domain.person import Person
from business_rules.domain.ride_registration import RideRegistration
from business_rules.domain.ride_registration_repository import (
    RideRegistrationRepository,
)
from business_rules.domain.static_context.policies.ride_attraction_admission_static_context_policy import (
    RideAttractionAdmissionStaticContextPolicy,
)
from business_rules.domain.static_context.ride_attraction_static_context import (
    RideAttractionStaticContext,
)
from business_rules.domain.weather import Weather
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder
from shared.domain.policies import Decision


class RideAttractionStaticContextPolicyCommandHandler(RideAttractionCommandHandler):
    def __init__(
        self,
        repo: RideRegistrationRepository,
        query_bus: QueryBus,
        metrics: MetricsRecorder,
    ) -> None:
        self._repo = repo
        self._query_bus = query_bus
        self._metrics = metrics
        self._ride_attraction_admission_policy = (
            RideAttractionAdmissionStaticContextPolicy.create(self._metrics)
        )
        self._decision_to_exception = {
            Decision.Outcome.DENY: AccessDenied,
            Decision.Outcome.WAIT: AccessTemporarilyDenied,
        }

    def handle(self, command: RideAttractionCommand) -> None:
        self._ensure_can_ride_attraction(command)

        registration = RideRegistration.create(
            person_id=command.person_id,
            attraction_id=command.attraction_id,
        )
        self._repo.save(registration)

    def _ensure_can_ride_attraction(self, command: RideAttractionCommand) -> None:
        context = self._get_ride_attraction_admission_policy_context(command)
        decision = self._ride_attraction_admission_policy.decide(context)
        if decision.is_allowed():
            return

        raise self._decision_to_exception[decision.outcome](decision.reason)

    def _get_person(self, command: RideAttractionCommand) -> Person:
        self._metrics.query("FindPerson")
        person = self._query_bus.ask(FindPersonQuery(person_id=command.person_id))
        assert person

        return person

    def _get_attraction(self, command: RideAttractionCommand) -> Attraction:
        self._metrics.query("FindAttraction")
        attraction = self._query_bus.ask(
            FindAttractionQuery(attraction_id=command.attraction_id)
        )
        assert attraction

        return attraction

    def _get_weather(self, command) -> Weather:
        self._metrics.query("FindCurrentWeather")
        weather = self._query_bus.ask(
            FindCurrentWeatherQuery(attraction_id=command.attraction_id)
        )
        assert weather

        return weather

    def _get_current_attraction_occupancy(
        self, command: RideAttractionCommand
    ) -> AttractionOccupancy:
        self._metrics.query("FindCurrentAttractionOccupancy")
        occupancy = self._query_bus.ask(
            FindCurrentAttractionOccupancyQuery(attraction_id=command.attraction_id)
        )
        assert occupancy

        return occupancy

    def _get_park_status(self, command: RideAttractionCommand):
        self._metrics.query("FindCurrentParkStatus")
        park_status = self._query_bus.ask(FindCurrentParkStatusQuery())
        assert park_status

        return park_status

    def _get_ride_attraction_admission_policy_context(
        self, command: RideAttractionCommand
    ) -> RideAttractionStaticContext:
        return RideAttractionStaticContext(
            person=self._get_person(command),
            attraction=self._get_attraction(command),
            weather=self._get_weather(command),
            occupancy=self._get_current_attraction_occupancy(command),
            park_status=self._get_park_status(command),
        )
