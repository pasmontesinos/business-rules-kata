from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Decision:
    class Outcome(Enum):
        DENY = "DENY"
        WAIT = "WAIT"
        ALLOW = "ALLOW"

    outcome: Decision.Outcome
    reason: str = ""

    @classmethod
    def allow(cls) -> Decision:
        return cls(Decision.Outcome.ALLOW, "")

    @classmethod
    def deny(cls, reason: str) -> Decision:
        return cls(Decision.Outcome.DENY, reason)

    @classmethod
    def wait(cls, reason: str) -> Decision:
        return cls(Decision.Outcome.WAIT, reason)

    def is_allowed(self) -> bool:
        return self.outcome == Decision.Outcome.ALLOW
