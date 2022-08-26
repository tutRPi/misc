from typing import Union, Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime, timedelta
from enum import Enum

from app.constants import ZONE_LOOKUP


class RateCodeID(int, Enum):
    STANDARD_RATE = 1
    JFK = 2
    NEWARK = 3
    NASSAU_WESTCHESTER = 4
    NEGOTIATED_FARE = 5
    GROUP_RIDE = 6


class PaymentType(int, Enum):
    CREDIT_CARD = 1
    CASH = 2
    NO_CHARGE = 3
    DISPUTE = 4
    UNKNOWN = 5
    VOIDED_TRIP = 6


class ReceiptCreate(BaseModel):
    VendorID: int = Field(alias="vendor_id")
    tpep_pickup_datetime: Union[int, str]
    tpep_dropoff_datetime: Union[int, str]
    passenger_count: int
    trip_distance: float
    PULocationID: int = Field(alias="pickup_location_id")  # Pickup zone
    DOLocationID: int = Field(alias="dropoff_location_id")  # Dropoff zone
    RatecodeID: RateCodeID = Field(alias="rate_code_id")
    store_and_fwd_flag: str = Field(exclude=True)
    payment_type: PaymentType
    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float
    improvement_surcharge: float
    total_amount: float
    congestion_surcharge: float
    airport_fee: float

    class Config:
        allow_population_by_field_name = True

    @validator('VendorID')
    def validate_vendor_id(cls, v):
        if v not in [1, 2]:
            raise ValueError('VendorID not in 1, 2')
        return v

    @validator('tpep_pickup_datetime', 'tpep_dropoff_datetime')
    def validate_datetime(cls, v):
        if type(v) == str:
            try:
                v = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                raise ValueError(e)
        elif type(v) == int:
            v = datetime.fromtimestamp(v // 1000)

        if datetime.now(v.tzinfo) + timedelta(days=1) < v:
            raise ValueError('Date is in the future')

        # v = v.isoformat()
        return v

    @validator('store_and_fwd_flag')
    def validate_store_and_fwd_flag(cls, v):
        if v not in ['Y', 'N']:
            raise ValueError('VendorID not in "Y" or "N"')
        return v

    @validator('PULocationID', 'DOLocationID')
    def validate_location_id(cls, v):
        # TODO change with db call
        if v not in ZONE_LOOKUP:
            raise ValueError('Invalid location id')
        return v

    @validator('airport_fee')
    def validate_airport_fee(cls, v):
        if v not in [0, 2.5]:
            raise ValueError('airport_fee not 0 or 2.5')
        return v

    @validator('fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount')
    def validate_positive_number(cls, v):
        if v < 0:
            raise ValueError('value is negative')
        return v


class ReceiptInDBBase(ReceiptCreate):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Receipt(ReceiptInDBBase):
    pass
