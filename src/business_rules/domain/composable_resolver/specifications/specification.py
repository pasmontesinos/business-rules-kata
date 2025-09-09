from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from shared.domain.specification_result import SpecificationResult

TResolver = TypeVar("TResolver", contravariant=True)


class Specification(Generic[TResolver], ABC):
    @abstractmethod
    def check(self, resolver: TResolver) -> SpecificationResult: ...
