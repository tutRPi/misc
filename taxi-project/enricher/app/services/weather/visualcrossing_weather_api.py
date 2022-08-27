import requests
from .weather_provider import *
from datetime import datetime, timezone, timedelta

from app.schemas.weather_data import WeatherDataCreate


class VisualcrossingWeatherApi(WeatherProvider):
    API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{formatted_date}"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_weather_data(self, location: str, date_time: datetime) -> WeatherDataCreate:
        formatted_date: str = date_time.strftime("%Y-%m-%d")
        url: str = self.API_URL.format(location=location, formatted_date=formatted_date)
        params = dict(
            unitGroup='metric',
            key=self.api_key,
            include='hours'
        )
        hour: int = date_time.hour
        resp = requests.get(url=url, params=params)
        data = resp.json()
        hourly_data = data["days"][0]["hours"][hour]

        # TODO check if timezone offset is needed or can be used from date_time
        new_datetime = datetime(date_time.year, date_time.month, date_time.day, hour, 0, 0, 0,
                                timezone(timedelta(seconds=data["tzoffset"] * 3600)))

        return WeatherDataCreate(**{
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "location": location,
            "resolved_address": data["resolvedAddress"],
            "datetime": new_datetime,
            "temperature_celsius": hourly_data["temp"],
            "humidity": hourly_data["humidity"],
            "precip": hourly_data["precip"],
            "description": hourly_data["icon"]
        })
