from __future__ import annotations

from business_rules.application import RideAttractionCommandHandler
from business_rules.application.commands.ride_attraction_command import (
    RideAttractionCommand,
)
from business_rules.domain.composable_resolver.policies.ride_attraction_admission_composable_resolver_policy import (
    RideAttractionAdmissionComposableResolverPolicy,
)
from business_rules.domain.composable_resolver.ride_attraction_composable_resolver import (
    RideAttractionComposableResolver,
)
from business_rules.domain.exceptions import AccessDenied, AccessTemporarilyDenied
from business_rules.domain.ride_registration import RideRegistration
from business_rules.domain.ride_registration_repository import (
    RideRegistrationRepository,
)
from shared.domain.metrics_recorder import MetricsRecorder
from shared.domain.policies import Decision


class RideAttractionComposableResolverPolicyCommandHandler(
    RideAttractionCommandHandler
):
    def __init__(
        self,
        repo: RideRegistrationRepository,
        context_resolver: RideAttractionComposableResolver,
        metrics: MetricsRecorder,
    ) -> None:
        self._repo = repo
        self._context_resolver = context_resolver
        self._metrics = metrics
        self._ride_attraction_admission_policy = (
            RideAttractionAdmissionComposableResolverPolicy.create(self._metrics)
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
        self._context_resolver.bind(
            person_id=command.person_id, attraction_id=command.attraction_id
        )
        decision = self._ride_attraction_admission_policy.decide(self._context_resolver)
        if decision.is_allowed():
            return

        raise self._decision_to_exception[decision.outcome](decision.reason)
