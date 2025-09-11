from dataclasses import dataclass

from business_rules.domain.attraction import Attraction
from business_rules.domain.occupancy import Occupancy
from business_rules.domain.park_status import ParkStatus
from business_rules.domain.person import Person
from business_rules.domain.weather import Weather


@dataclass(frozen=True)
class RideAttractionStaticContext:
    person: Person
    attraction: Attraction
    weather: Weather
    occupancy: Occupancy
    park_status: ParkStatus
