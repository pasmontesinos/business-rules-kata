from __future__ import annotations

from unittest.mock import create_autospec
import pytest

from business_rules.application.commands.composable_resolver.ride_attraction_composable_resolver_policy import (
    RideAttractionComposableResolverPolicyCommandHandler,
)
from business_rules.application.commands.context_resolver.ride_attraction_context_resolver_policy import (
    RideAttractionContextResolverPolicyCommandHandler,
)
from business_rules.application.commands.ride_attraction_command import (
    RideAttractionCommand,
)

from business_rules.application.commands.sequential.ride_attraction_sequential_lumper_style_rules_command_handler import (
    RideAttractionSequentialLumperStyleRulesCommandHandler,
)
from business_rules.application.commands.sequential.ride_attraction_sequential_specs_style_rules_command_handler import (
    RideAttractionSequentialSpecsStyleRulesCommandHandler,
)
from business_rules.application.commands.sequential.ride_attraction_sequential_splitter_style_rules_command_handler import (
    RideAttractionSequentialSplitterStyleRulesCommandHandler,
)
from business_rules.application.commands.static_context.ride_attraction_static_context_policy import (
    RideAttractionStaticContextPolicyCommandHandler,
)
from business_rules.domain.exceptions import AccessDenied
from business_rules.domain.exceptions import AccessTemporarilyDenied
from business_rules.application.queries.find_person import (
    FindPersonQuery,
)
from business_rules.domain.person import Person
from business_rules.application.queries.find_current_weather import (
    FindCurrentWeatherQuery,
)
from business_rules.application.queries.find_current_attraction_occupancy import (
    FindCurrentAttractionOccupancyQuery,
)
from business_rules.application.queries.find_attraction import (
    FindAttractionQuery,
)
from business_rules.domain.ride_registration_repository import (
    RideRegistrationRepository,
)
from business_rules.infrastructure.composable_resolver.ride_attraction_lazy_composable_resolver import (
    LazyRideAttractionComposableResolver,
)
from business_rules.infrastructure.context_resolver.ride_attraction_lazy_context_resolver import (
    LazyRideAttractionContextResolver,
)
from shared.infrastructure import FakeQueryBus
from shared.infrastructure.in_memory_metrics_recorder import InMemoryMetricsRecorder
from tests.shared.infrastructure.get_call_param import get_call_param
from business_rules.domain.weather import Weather
from business_rules.domain.attraction_occupancy import AttractionOccupancy
from business_rules.domain.attraction import Attraction
from business_rules.domain.park_status import ParkStatus
from business_rules.application.queries.find_current_park_status import (
    FindCurrentParkStatusQuery,
)

PERSON_ID = "p1"
LOW_HEIGHT_PERSON_ID = "p2"
ATTRACTION_ID = "a1"


@pytest.mark.parametrize(
    "handler_cls",
    [
        RideAttractionSequentialSplitterStyleRulesCommandHandler,
        RideAttractionSequentialLumperStyleRulesCommandHandler,
        RideAttractionSequentialSpecsStyleRulesCommandHandler,
        RideAttractionStaticContextPolicyCommandHandler,
        RideAttractionContextResolverPolicyCommandHandler,
        RideAttractionComposableResolverPolicyCommandHandler,
    ],
    scope="function",
)
class TestRideAttractionCommandHandler:
    @pytest.fixture(autouse=True)
    def _setup(self, handler_cls, request):
        self._handler_cls = handler_cls
        self._request = request
        self._repo = create_autospec(
            RideRegistrationRepository, spec_set=True, instance=True
        )

        self._metrics = InMemoryMetricsRecorder()
        self._query_bus = self._build_query_bus()
        self._command_handler = self._build_command_handler()

    def teardown_method(self, method):
        self._print_metrics()

    def test_should_create_ride_registration(self) -> None:
        self._command_handler.handle(
            RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
        )

        saved = get_call_param(self._repo.save)
        assert saved.person_id == PERSON_ID
        assert saved.attraction_id == ATTRACTION_ID

    def test_should_deny_access_when_person_height_is_below_minimum(self) -> None:
        self._query_bus.query_to_result(
            FindPersonQuery(person_id=LOW_HEIGHT_PERSON_ID),
            Person(person_id=LOW_HEIGHT_PERSON_ID, height_cm=119),
        )

        with pytest.raises(AccessDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(
                    person_id=LOW_HEIGHT_PERSON_ID, attraction_id=ATTRACTION_ID
                )
            )

        assert str(exc.value) == "Person height below minimum"

    def test_should_deny_temporarily_access_when_adverse_weather(self) -> None:
        self._query_bus.query_to_result(
            FindCurrentWeatherQuery(attraction_id=ATTRACTION_ID),
            Weather(is_adverse=True),
        )

        with pytest.raises(AccessTemporarilyDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
            )

        assert str(exc.value) == "Adverse weather"

    def test_should_deny_temporarily_access_when_under_maintenance(self) -> None:
        self._query_bus.query_to_result(
            FindAttractionQuery(attraction_id=ATTRACTION_ID),
            Attraction(is_under_maintenance=True),
        )

        with pytest.raises(AccessTemporarilyDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
            )

        assert str(exc.value) == "Under maintenance, please wait"

    def test_should_prioritize_access_denied_over_temporarily_denied_on_conflict(
        self,
    ) -> None:
        self._query_bus.query_to_result(
            FindCurrentWeatherQuery(attraction_id=ATTRACTION_ID),
            Weather(is_adverse=True),
        )
        self._query_bus.query_to_result(
            FindPersonQuery(person_id=PERSON_ID),
            Person(person_id=PERSON_ID, height_cm=119),
        )

        with pytest.raises(AccessDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
            )
        assert str(exc.value) == "Person height below minimum"

    def test_should_deny_access_temporarily_when_full_capacity(self) -> None:
        self._query_bus.query_to_result(
            FindCurrentAttractionOccupancyQuery(attraction_id=ATTRACTION_ID),
            AttractionOccupancy(current_occupancy=10, capacity=10),
        )

        with pytest.raises(AccessTemporarilyDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
            )

        assert str(exc.value) == "Attraction at full capacity"

    def test_should_deny_access_when_attraction_is_closed(self) -> None:
        self._query_bus.query_to_result(
            FindAttractionQuery(attraction_id=ATTRACTION_ID),
            Attraction(is_under_maintenance=False, closed=True),
        )

        with pytest.raises(AccessDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
            )

        assert str(exc.value) == "Attraction closed"

    def test_should_deny_access_when_peak_hours_popular_without_fast_pass(self) -> None:
        self._query_bus.query_to_result(
            FindPersonQuery(person_id=PERSON_ID),
            Person(person_id=PERSON_ID, height_cm=120, has_fast_pass=False),
        )

        with pytest.raises(AccessDenied) as exc:
            self._command_handler.handle(
                RideAttractionCommand(person_id=PERSON_ID, attraction_id=ATTRACTION_ID)
            )

        assert (
            str(exc.value)
            == "Fast pass required during peak hours for popular attractions"
        )

    def _print_metrics(self):
        print(
            f"{self._request.node.name} effort: ",
            self._metrics.total_effort,
            # self._metrics.detail,
        )

    def _build_query_bus(self) -> FakeQueryBus:
        return FakeQueryBus(
            {
                FindPersonQuery(person_id=PERSON_ID): Person(
                    person_id=PERSON_ID, height_cm=120, has_fast_pass=True
                ),
                FindAttractionQuery(attraction_id=ATTRACTION_ID): Attraction(
                    is_under_maintenance=False, is_popular=True
                ),
                FindCurrentWeatherQuery(attraction_id=ATTRACTION_ID): Weather(
                    is_adverse=False
                ),
                FindCurrentAttractionOccupancyQuery(
                    attraction_id=ATTRACTION_ID
                ): AttractionOccupancy(current_occupancy=0, capacity=10),
                FindCurrentParkStatusQuery(): ParkStatus(peak_hours=True),
            }
        )

    def _build_command_handler(self):
        if self._handler_cls == RideAttractionContextResolverPolicyCommandHandler:
            return self._handler_cls(
                repo=self._repo,
                context_resolver=LazyRideAttractionContextResolver(
                    query_bus=self._query_bus, metrics=self._metrics
                ),
                metrics=self._metrics,
            )

        if self._handler_cls == RideAttractionComposableResolverPolicyCommandHandler:
            return self._handler_cls(
                repo=self._repo,
                context_resolver=LazyRideAttractionComposableResolver(
                    query_bus=self._query_bus, metrics=self._metrics
                ),
                metrics=self._metrics,
            )

        return self._handler_cls(
            repo=self._repo, query_bus=self._query_bus, metrics=self._metrics
        )
