from abc import ABC, abstractmethod

from business_rules.domain.weather import Weather


class WeatherResolver(ABC):
    @property
    @abstractmethod
    def weather(self) -> Weather: ...
