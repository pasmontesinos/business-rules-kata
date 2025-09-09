from business_rules.application.queries.find_person import FindPersonQuery
from business_rules.domain.person import Person
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class QueryPersonResolver:
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics
        self._person_id: str | None = None
        self._person: Person | None = None

    def bind(self, person_id: str) -> None:
        self._person_id = person_id
        self._person = None

    @property
    def person(self) -> Person:
        if self._person:
            return self._person

        assert self._person_id is not None

        self._metrics.query("FindPerson")
        self._person = self._query_bus.ask(FindPersonQuery(person_id=self._person_id))

        assert self._person is not None
        return self._person
