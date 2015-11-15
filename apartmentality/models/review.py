from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.schema import Column, ForeignKey, UniqueConstraint, \
    ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text
from apartmentality.database import Base
from apartmentality.models.tag import Tag


class ReviewTag(Base):
    __tablename__ = "review_tags"
    __table_args__ = (
        ForeignKeyConstraint(["property_id", "user_id"],
                             ["reviews.property_id", "reviews.user_id"]),
    )

    tag_id = Column(ForeignKey("tags.id"), primary_key=True)
    property_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)


class Review(Base):
    __tablename__ = "reviews"

    user_id = Column(ForeignKey("users.id"), primary_key=True)
    property_id = Column(ForeignKey("properties.id"), primary_key=True)
    manager_id = Column(ForeignKey("managers.id"))

    unit = Column(String(50))
    date = Column(DateTime, index=True)

    rent = Column(Integer)

    rating_kitchen = Column(Integer, index=True)
    rating_bedroom = Column(Integer, index=True)
    rating_bathroom = Column(Integer, index=True)
    rating_area = Column(Integer, index=True)
    rating_average = Column(Integer, index=True)

    text = Column(Text)

    user = relationship("User", backref="reviews")
    property = relationship("Property", backref="reviews")
    manager = relationship("Manager", backref="properties")

    tags = relationship(
        "Tag",
        secondary=ReviewTag.__table__,
        primaryjoin=and_(
            user_id == ReviewTag.user_id,
            property_id == ReviewTag.property_id,
        ),
        secondaryjoin=and_(
            ReviewTag.tag_id == Tag.id,
        )
    )
