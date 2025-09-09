from business_rules.application.queries.find_current_weather import (
    FindCurrentWeatherQuery,
)
from business_rules.domain.composable_resolver.weather_resolver import WeatherResolver
from business_rules.domain.weather import Weather
from shared.application import QueryBus
from shared.domain.metrics_recorder import MetricsRecorder


class QueryWeatherResolver(WeatherResolver):
    def __init__(self, query_bus: QueryBus, metrics: MetricsRecorder) -> None:
        self._query_bus = query_bus
        self._metrics = metrics
        self._attraction_id: str | None = None
        self._weather: Weather | None = None

    def bind(self, attraction_id: str) -> None:
        self._attraction_id = attraction_id
        self._weather = None

    @property
    def weather(self) -> Weather:
        if self._weather:
            return self._weather

        assert self._attraction_id is not None

        self._metrics.query("FindCurrentWeather")
        self._weather = self._query_bus.ask(
            FindCurrentWeatherQuery(attraction_id=self._attraction_id)
        )

        assert self._weather is not None
        return self._weather
