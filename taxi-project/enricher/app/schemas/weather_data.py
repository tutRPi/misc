from typing import Union, Optional

import datetime as datetime
from pydantic import BaseModel
from datetime import datetime


class WeatherDataCreate(BaseModel):
    latitude: float
    longitude: float
    location: str
    resolved_address: str
    datetime: datetime
    temperature_celsius: float
    humidity: float
    precip: float
    description: str
    
    country: Optional[str] = None
    city: Optional[str] = None


class WeatherDataInDBBase(WeatherDataCreate):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class WeatherData(WeatherDataInDBBase):
    pass
