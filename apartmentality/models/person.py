"""Person table.
"""
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from apartmentality.database import Base


class Person(Base):
    """Represents a person.
    """

    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    middle_initial = Column(String(1))
    last_name = Column(String(50))
    email = Column(String(254), unique=True, index=True)
