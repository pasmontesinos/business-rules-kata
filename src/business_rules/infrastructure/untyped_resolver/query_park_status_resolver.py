from business_rules.application.queries.find_current_park_status import (
    FindCurrentParkStatusQuery,
)
from business_rules.domain.park_status import ParkStatus
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class QueryParkStatusResolver:
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics
        self._park_status: ParkStatus | None = None

    def bind(self) -> None:
        self._park_status = None

    @property
    def park_status(self) -> ParkStatus:
        if self._park_status:
            return self._park_status

        self._metrics.query("FindCurrentParkStatus")
        self._park_status = self._query_bus.ask(FindCurrentParkStatusQuery())

        assert self._park_status is not None
        return self._park_status
