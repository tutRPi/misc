from app.crud.base import CRUDBase
from app.models.location import Location
from app.schemas.location import LocationCreate


class CRUDLocation(CRUDBase[Location, LocationCreate, None]):
    pass


location = CRUDLocation(Location)
