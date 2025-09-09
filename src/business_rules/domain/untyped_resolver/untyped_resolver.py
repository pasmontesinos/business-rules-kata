from __future__ import annotations

from abc import abstractmethod
from typing import Any


class UntypedResolver:
    @abstractmethod
    def bind(self, *args: Any, **kwargs: Any) -> None: ...

    @abstractmethod
    def resolve(self, key: str) -> Any: ...
