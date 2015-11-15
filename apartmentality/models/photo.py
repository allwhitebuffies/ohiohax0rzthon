from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Binary, String

from apartmentality.database import Base


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    property_id = Column(ForeignKey("properties.id"))
    url = Column(String(255))

    property = relationship("Property", backref="photos")
