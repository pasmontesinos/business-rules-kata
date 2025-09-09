from abc import ABC, abstractmethod

from business_rules.domain.attraction_occupancy import AttractionOccupancy


class OccupancyResolver(ABC):
    @property
    @abstractmethod
    def occupancy(self) -> AttractionOccupancy: ...
