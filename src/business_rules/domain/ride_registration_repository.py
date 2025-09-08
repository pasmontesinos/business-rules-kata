from __future__ import annotations

from abc import ABC

from business_rules.domain.ride_registration import RideRegistration


class RideRegistrationRepository(ABC):
    def save(self, registration: RideRegistration) -> None: ...
