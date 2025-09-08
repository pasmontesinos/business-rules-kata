from __future__ import annotations

from typing import Mapping
from abc import ABC, abstractmethod


class MetricsRecorder(ABC):
    @property
    @abstractmethod
    def total_effort(self) -> int:
        raise NotImplementedError

    @property
    @abstractmethod
    def detail(self) -> Mapping[str, int]:
        raise NotImplementedError

    @abstractmethod
    def rule(self, name: str) -> None: ...

    @abstractmethod
    def query(self, name: str) -> None: ...
