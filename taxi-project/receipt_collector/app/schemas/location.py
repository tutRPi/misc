from typing import Union, Optional
from pydantic import BaseModel


class LocationCreate(BaseModel):
    id: Union[int, None]
    country: str
    city: str
    borough: Union[str, None]
    zone: Union[str, None]


class LocationInDBBase(LocationCreate):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Location(LocationInDBBase):
    pass
