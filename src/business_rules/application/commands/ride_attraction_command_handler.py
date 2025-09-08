from __future__ import annotations

from business_rules.application.commands.ride_attraction_command import (
    RideAttractionCommand,
)
from abc import ABC, abstractmethod


class RideAttractionCommandHandler(ABC):
    @abstractmethod
    def handle(self, command: RideAttractionCommand) -> None: ...
