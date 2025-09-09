from abc import ABC, abstractmethod

from business_rules.domain.park_status import ParkStatus


class ParkStatusResolver(ABC):
    @property
    @abstractmethod
    def park_status(self) -> ParkStatus: ...
