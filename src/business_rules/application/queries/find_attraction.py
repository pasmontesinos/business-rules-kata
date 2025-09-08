from __future__ import annotations

from dataclasses import dataclass
from shared.application import Query


@dataclass(frozen=True)
class FindAttractionQuery(Query):
    attraction_id: str
