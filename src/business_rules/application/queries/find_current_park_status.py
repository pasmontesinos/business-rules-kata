from __future__ import annotations

from dataclasses import dataclass
from shared.application import Query


@dataclass(frozen=True)
class FindCurrentParkStatusQuery(Query):
    pass
