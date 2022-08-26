from sqlalchemy.orm import Session

from app import crud, schemas

from app.constants import ZONE_LOOKUP
from app.db import base


def init_db(db: Session) -> None:
    base.Base.metadata.create_all(bind=base.engine)

    for zone_id, zone in ZONE_LOOKUP.items():
        location = crud.location.get(db, zone_id)
        if not location:
            location_in = schemas.location.LocationCreate(
                id=zone_id,
                country="US",
                city="New York",
                borough=zone["Borough"],
                zone=zone["Zone"],
            )
            location = crud.location.create(db=db, obj_in=location_in)
            print("Created location with id", location.id)
