from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from apartmentality.database import Base


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True)
    phone = Column(String(50))
    street_number = Column(Integer)
    street_name = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip = Column(Integer)

    company_id = Column(ForeignKey("companies.id"))
    person_id = Column(ForeignKey("people.id"))

    company = relationship("Company")
    person = relationship("Person")
