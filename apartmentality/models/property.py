from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from apartmentality.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    city = Column(String(50), index=True)
    state = Column(String(50), index=True)
    zip = Column(Integer, index=True)
    street_number = Column(Integer, index=True)
    street_name = Column(String(50), index=True)
    type = Column(String(50), index=True)
    unit = Column(String(50), index=True)
