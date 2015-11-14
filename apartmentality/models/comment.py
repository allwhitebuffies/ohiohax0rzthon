from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Text, DateTime

from apartmentality.database import Base


class Comment(Base):
    __tablename__ = "comments"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    property_id = Column(ForeignKey("properties.id"), primary_key=True)
    text = Column(Text)
    date = Column(DateTime, index=True)
