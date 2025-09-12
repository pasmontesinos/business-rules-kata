from __future__ import annotations

from dataclasses import dataclass

from shared.application.command import Command


@dataclass(frozen=True)
class RideAttractionCommand(Command):
    person_id: str
    attraction_id: str
    country_code: str
