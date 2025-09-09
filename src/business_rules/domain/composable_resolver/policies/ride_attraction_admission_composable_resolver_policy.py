from __future__ import annotations

from business_rules.domain.composable_resolver.ride_attraction_composable_resolver import (
    RideAttractionComposableResolver,
)

from business_rules.domain.composable_resolver.specifications.has_capacity_available_specification import (
    HasCapacityAvailableSpecification,
)
from business_rules.domain.composable_resolver.specifications.has_favorable_weather_specification import (
    HasFavorableWeatherSpecification,
)
from business_rules.domain.composable_resolver.specifications.is_attraction_open_specification import (
    IsAttractionOpenSpecification,
)
from business_rules.domain.composable_resolver.specifications.is_attraction_operational_specification import (
    IsAttractionOperationalSpecification,
)
from business_rules.domain.composable_resolver.specifications.is_tall_enough_specification import (
    IsTallEnoughSpecification,
)
from business_rules.domain.composable_resolver.specifications.requires_fast_pass_during_peak_for_popular_specification import (
    RequiresFastPassDuringPeakForPopularSpecification,
)
from business_rules.domain.composable_resolver.specifications.specification import (
    Specification,
)

from shared.domain.metrics_recorder import MetricsRecorder
from shared.domain.policies import Decision


class RideAttractionAdmissionComposableResolverPolicy:
    def __init__(
        self,
        metrics_recorder: MetricsRecorder,
        specs_to_unsatisfied_outcome: dict[
            Specification[RideAttractionComposableResolver], Decision.Outcome
        ],
    ) -> None:
        self._metrics_recorder = metrics_recorder
        self._specs_to_unsatisfied_outcome = specs_to_unsatisfied_outcome

    @classmethod
    def create(
        cls, metrics_recorder: MetricsRecorder
    ) -> RideAttractionAdmissionComposableResolverPolicy:
        return cls(
            metrics_recorder=metrics_recorder,
            specs_to_unsatisfied_outcome={
                IsTallEnoughSpecification(): Decision.Outcome.DENY,
                IsAttractionOpenSpecification(): Decision.Outcome.DENY,
                RequiresFastPassDuringPeakForPopularSpecification(): Decision.Outcome.DENY,
                IsAttractionOperationalSpecification(): Decision.Outcome.WAIT,
                HasFavorableWeatherSpecification(): Decision.Outcome.WAIT,
                HasCapacityAvailableSpecification(): Decision.Outcome.WAIT,
            },
        )

    def decide(self, context: RideAttractionComposableResolver) -> Decision:
        for specification, outcome in self._specs_to_unsatisfied_outcome.items():
            self._metrics_recorder.rule(specification.__class__.__name__)
            spec_result = specification.check(context)
            if not spec_result.satisfied:
                return Decision(outcome, spec_result.reason)

        return Decision.allow()
