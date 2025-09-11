from __future__ import annotations

from abc import ABC, abstractmethod
from business_rules.domain.person import Person
from business_rules.domain.weather import Weather
from business_rules.domain.occupancy import Occupancy
from business_rules.domain.attraction import Attraction
from business_rules.domain.park_status import ParkStatus


class RideAttractionContextResolver(ABC):
    @abstractmethod
    def bind(self, person_id: str, attraction_id: str) -> None: ...

    @property
    @abstractmethod
    def person(self) -> Person: ...

    @property
    @abstractmethod
    def weather(self) -> Weather: ...

    @property
    @abstractmethod
    def occupancy(self) -> Occupancy: ...

    @property
    @abstractmethod
    def attraction(self) -> Attraction: ...

    @property
    @abstractmethod
    def park_status(self) -> ParkStatus: ...
