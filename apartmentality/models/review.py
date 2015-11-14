from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer

from apartmentality.database import Base


class Review(Base):
    __tablename__ = "reviews"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    property_id = Column(ForeignKey("properties.id"), primary_key=True)
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)

    rent = Column(Integer)

    rating_kitchen = Column(Integer, index=True)
    rating_bedroom = Column(Integer, index=True)
    rating_bathroom = Column(Integer, index=True)
    rating_area = Column(Integer, index=True)
    rating_average = Column(Integer, index=True)
