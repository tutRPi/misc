import abc
from datetime import datetime
from typing import List

from app.schemas.weather_data import WeatherDataCreate


class WeatherProvider(abc.ABC):
    @abc.abstractmethod
    def get_weather_data(self, location: str, date_time: datetime) -> List[WeatherDataCreate]:
        pass
