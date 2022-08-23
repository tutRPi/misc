import abc
from datetime import datetime


class WeatherData:
    def __init__(self, location: str, date_time: datetime, temperature_celsius: float, humidity: float, precip: float):
        self.location = location
        self.datetime = date_time
        self.temperature_celsius = temperature_celsius
        self.humidity = humidity
        self.precip = precip

    def __str__(self):
        return "WeatherData(location={location}, datetime={datetime}, temperature_celsius={temperature_celsius}, humidity={humidity}, precip={precip})" \
            .format(location=self.location, datetime=self.datetime, temperature_celsius=self.temperature_celsius,
                    humidity=self.humidity, precip=self.precip)


class WeatherProvider(abc.ABC):
    @abc.abstractmethod
    def get_weather_data(self, location: str, date_time: datetime) -> WeatherData:
        pass
