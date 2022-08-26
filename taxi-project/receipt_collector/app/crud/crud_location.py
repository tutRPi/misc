from app.crud.base import CRUDBase
from app.models.location import Location
from app.schemas.location import LocationCreate


class CRUDRLocation(CRUDBase[Location, LocationCreate, None]):
    pass


location = CRUDRLocation(Location)
