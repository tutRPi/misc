from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Location(Base):
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    city = Column(String)
    borough = Column(String, nullable=True)
    zone = Column(String, nullable=True)
