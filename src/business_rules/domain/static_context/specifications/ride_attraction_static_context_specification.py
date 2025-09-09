from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from business_rules.domain.static_context.ride_attraction_static_context import (
    RideAttractionStaticContext,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class RideAttractionStaticContextSpecification(ABC):
    @abstractmethod
    def check(self, context: RideAttractionStaticContext) -> SpecificationResult: ...
