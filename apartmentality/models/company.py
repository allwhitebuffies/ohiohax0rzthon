from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from apartmentality.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(254))
