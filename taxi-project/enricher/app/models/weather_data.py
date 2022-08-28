from sqlalchemy import Column, Integer, String, Float, DateTime

from app.db.base_class import Base
from app.models.custom_datetime import CustomDateTime


class WeatherData(Base):
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    location = Column(String, index=True)
    resolved_address = Column(String)
    datetime = Column(CustomDateTime)
    temperature_celsius = Column(Float)
    humidity = Column(Float)
    precip = Column(Float)
    description = Column(String)

    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
