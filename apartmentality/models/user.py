from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from apartmentality.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    hash = Column(String(64))
    salt = Column(String(32))
    person_id = Column(ForeignKey("people.id"), index=True, nullable=False)

    person = relationship("Person")
