from business_rules.application.queries.find_current_attraction_occupancy import (
    FindCurrentAttractionOccupancyQuery,
)
from business_rules.domain.occupancy import Occupancy
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class QueryOccupancyResolver:
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics
        self._attraction_id: str | None = None
        self._occupancy: Occupancy | None = None

    def bind(self, attraction_id: str) -> None:
        self._attraction_id = attraction_id
        self._occupancy = None

    @property
    def occupancy(self) -> Occupancy:
        if self._occupancy:
            return self._occupancy

        assert self._attraction_id is not None

        self._metrics.query("FindCurrentAttractionOccupancy")
        self._occupancy = self._query_bus.ask(
            FindCurrentAttractionOccupancyQuery(attraction_id=self._attraction_id)
        )

        assert self._occupancy is not None
        return self._occupancy
