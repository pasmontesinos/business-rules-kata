from abc import ABC, abstractmethod

from business_rules.domain.occupancy import Occupancy


class OccupancyResolver(ABC):
    @property
    @abstractmethod
    def occupancy(self) -> Occupancy: ...
