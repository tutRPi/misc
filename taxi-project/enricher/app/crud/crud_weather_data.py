import datetime
from typing import Optional

from sqlalchemy import and_, extract

from app.crud.base import CRUDBase
from app.models.weather_data import WeatherData
from app.schemas.weather_data import WeatherDataCreate

from sqlalchemy.orm import Session


class CRUDWeatherData(CRUDBase[WeatherData, WeatherDataCreate, None]):
    def get_by_location(self, db: Session, location: str, date_time: datetime.datetime) -> Optional[WeatherData]:
        return db.query(self.model).filter(
            and_(self.model.location == location,
                 date_time.year == extract('year', self.model.datetime),
                 date_time.month == extract('month', self.model.datetime),
                 date_time.day == extract('day', self.model.datetime),
                 date_time.hour == extract('hour', self.model.datetime),
                 )).first()


weather_data = CRUDWeatherData(WeatherData)
