from abc import ABC, abstractmethod

from business_rules.domain.untyped_resolver.untyped_resolver import UntypedResolver
from shared.domain.specification_result import SpecificationResult


class UntypedResolverSpecification(ABC):
    @abstractmethod
    def check(self, resolver: UntypedResolver) -> SpecificationResult: ...
