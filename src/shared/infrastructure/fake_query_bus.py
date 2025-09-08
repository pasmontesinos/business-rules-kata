from __future__ import annotations

from shared.application.query import Query, QueryBus


class FakeQueryBus(QueryBus):
    def __init__(self, queries_to_results: dict[Query, object] | None = None) -> None:
        self._query_to_result: dict[Query, object] = dict(queries_to_results or {})

    def ask(self, query: Query) -> object:
        if query not in self._query_to_result:
            raise ValueError(f"Unexpected query: {query!r}")

        return self._query_to_result[query]

    def query_to_result(self, query: Query, result: object) -> None:
        self._query_to_result[query] = result
