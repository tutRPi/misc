from typing import Union, Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime, timedelta
from enum import Enum

from app.constants import ZONE_LOOKUP
from .location import Location

# explanation for validations: https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf


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

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class ReceiptBase(BaseModel):
    tpep_pickup_datetime: Union[int, str, datetime]
    tpep_dropoff_datetime: Union[int, str, datetime]
    passenger_count: Union[int, None]
    trip_distance: float
    RatecodeID: int = Field(alias="rate_code_id")  # Union[RateCodeID, None] = Field(alias="rate_code_id")
    payment_type: Union[int, None] = PaymentType.UNKNOWN
    fare_amount: float
    extra: float
    mta_tax: float
    tip_amount: float
    tolls_amount: float = 0
    improvement_surcharge: float
    total_amount: float
    congestion_surcharge: Union[float, None]
    airport_fee: Union[float, None]

    class Config:
        allow_population_by_field_name = True


class ReceiptCreate(ReceiptBase):
    VendorID: Union[int, None] = Field(alias="vendor_id")
    PULocationID: int = Field(alias="pickup_location_id")  # Pickup zone
    DOLocationID: int = Field(alias="dropoff_location_id")  # Dropoff zone
    store_and_fwd_flag: Union[str, None] = Field(exclude=True)

    @validator('VendorID')
    def validate_vendor_id(cls, v):
        if v is not None and v not in [1, 2]:
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
        if v is not None and v not in ['Y', 'N']:
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
        if v is not None and v not in [0, 1.25]:
            raise ValueError('airport_fee not 0 or 1.25')
        return v

    @validator('payment_type')
    def validate_payment_type(cls, v):
        if v is None or not PaymentType.has_value(v):
            v = PaymentType.UNKNOWN
        return v

    @validator('passenger_count', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount')
    def validate_positive_number(cls, v):
        if v is not None and v < 0:
            raise ValueError('value is negative')
        return v


class ReceiptInDBBase(ReceiptCreate):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Receipt(ReceiptInDBBase):
    pass


class ReceiptForwardMessage(ReceiptBase):
    pickup_location: Location
    dropoff_location: Location

    class Config:
        orm_mode = True
