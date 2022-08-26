from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.custom_datetime import CustomDateTime


class Receipt(Base):
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer)
    tpep_pickup_datetime = Column(CustomDateTime)
    tpep_dropoff_datetime = Column(CustomDateTime)
    passenger_count = Column(Integer)
    trip_distance = Column(Numeric(10, 2))
    pickup_location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    dropoff_location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    rate_code_id = Column(Integer)
    payment_type = Column(Integer)
    fare_amount = Column(Numeric(10, 2))
    extra = Column(Numeric(10, 2))
    mta_tax = Column(Numeric(10, 2))
    tip_amount = Column(Numeric(10, 2))
    tolls_amount = Column(Numeric(10, 2))
    improvement_surcharge = Column(Numeric(10, 2))
    total_amount = Column(Numeric(10, 2))
    congestion_surcharge = Column(Numeric(10, 2))
    airport_fee = Column(Numeric(10, 2))

    pickup_location = relationship("Location", foreign_keys=[pickup_location_id])
    dropoff_location = relationship("Location", foreign_keys=[dropoff_location_id])
