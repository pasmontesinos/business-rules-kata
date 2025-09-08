from __future__ import annotations

from dataclasses import dataclass
from shared.application.query import Query


@dataclass(frozen=True)
class FindPersonQuery(Query):
    person_id: str
