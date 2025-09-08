from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class RideRegistration:
    ride_registration_id: str
    person_id: str
    attraction_id: str

    @classmethod
    def create(cls, person_id: str, attraction_id: str) -> RideRegistration:
        ride_registration_id = str(uuid.uuid4())
        return cls(ride_registration_id, person_id, attraction_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RideRegistration):
            return NotImplemented

        return self.ride_registration_id == other.ride_registration_id
