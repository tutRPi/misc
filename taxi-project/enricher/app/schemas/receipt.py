from typing import Union
from pydantic import BaseModel
from datetime import datetime


class ReceiptForBigQuery(BaseModel):
    tpep_pickup_datetime: datetime
    tpep_dropoff_datetime: datetime

    passenger_count: int
    trip_distance: float
    best_route_distance: Union[float, None]
    #    rate_code_id: int
    payment_type: int
    #    fare_amount: float
    #    extra: float
    #    mta_tax: float
    tip_amount: float
    #    tolls_amount: float
    #    improvement_surcharge: float
    total_amount: float
    #    congestion_surcharge: float
    #    airport_fee: float

    pickup_city: str
    pickup_country: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_latitude: Union[float, None]
    dropoff_longitude: Union[float, None]

    temperature_celsius: float
    humidity: float
    precip: float
    weather_description: str
