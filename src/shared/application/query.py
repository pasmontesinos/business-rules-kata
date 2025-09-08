from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Query: ...


class QueryBus(ABC):
    @abstractmethod
    def ask(self, query: Query) -> Any: ...
