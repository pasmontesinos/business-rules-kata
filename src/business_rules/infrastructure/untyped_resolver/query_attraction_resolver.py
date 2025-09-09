from business_rules.application.queries.find_attraction import FindAttractionQuery
from business_rules.domain.attraction import Attraction
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class QueryAttractionResolver:
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics
        self._attraction_id: str | None = None
        self._attraction: Attraction | None = None

    def bind(self, attraction_id: str) -> None:
        self._attraction_id = attraction_id
        self._attraction = None

    @property
    def attraction(self) -> Attraction:
        if self._attraction:
            return self._attraction

        assert self._attraction_id is not None

        self._metrics.query("FindAttraction")
        self._attraction = self._query_bus.ask(
            FindAttractionQuery(attraction_id=self._attraction_id)
        )

        assert self._attraction is not None
        return self._attraction
