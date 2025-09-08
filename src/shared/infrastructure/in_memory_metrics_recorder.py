from __future__ import annotations

from typing import Mapping, Dict

from shared.domain.metrics_recorder import MetricsRecorder


class InMemoryMetricsRecorder(MetricsRecorder):
    RULE_EXECUTION_EFFORT: int = 1
    QUERY_EXECUTION_EFFORT: int = 1000

    def __init__(self) -> None:
        self._detail: Dict[str, int] = {}
        self._total: int = 0

    @property
    def total_effort(self) -> int:
        return self._total

    @property
    def detail(self) -> Mapping[str, int]:
        return self._detail

    def rule(self, name: str) -> None:
        self._record_key(
            key=f"rule::{name}",
            value=self.RULE_EXECUTION_EFFORT,
        )

    def query(self, name: str) -> None:
        self._record_key(
            key=f"query::{name}",
            value=self.QUERY_EXECUTION_EFFORT,
        )

    def _record_key(self, key: str, value: int) -> None:
        self._detail[key] = self._detail.get(key, 0) + value
        self._total += value
