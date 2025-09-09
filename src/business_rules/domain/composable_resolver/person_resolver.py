from abc import ABC, abstractmethod

from business_rules.domain.person import Person


class PersonResolver(ABC):
    @property
    @abstractmethod
    def person(self) -> Person: ...
