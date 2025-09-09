from abc import ABC, abstractmethod

from business_rules.domain.attraction import Attraction


class AttractionResolver(ABC):
    @property
    @abstractmethod
    def attraction(self) -> Attraction: ...
