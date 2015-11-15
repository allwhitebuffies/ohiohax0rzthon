from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from apartmentality.database import Base


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True)
