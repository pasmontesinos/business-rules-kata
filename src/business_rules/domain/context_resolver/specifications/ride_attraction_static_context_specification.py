from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from business_rules.domain.context_resolver.ride_attraction_context_resolver import (
    RideAttractionContextResolver,
)
from shared.domain.specification_result import SpecificationResult


@dataclass(frozen=True)
class RideAttractionContextResolverSpecification(ABC):
    @abstractmethod
    def check(self, context: RideAttractionContextResolver) -> SpecificationResult: ...
