from apartmentality.database import DBSession
from apartmentality.models.review import Review
from apartmentality.views import Resource


class ReviewDispatcher(Resource):
    def __getitem__(self, item):
        obj = ReviewResource(self.request, item)
        obj.__name__ = item
        obj.__parent__ = self
        return obj


class ReviewResource(Resource):
    def __init__(self, request, review_id):
        super().__init__(request)

        prop_id, part, user_id = review_id.partition("-")

        if part == "":
            raise KeyError(review_id)

        try:
            prop_id = int(prop_id)
            user_id = int(user_id)
        except ValueError:
            raise KeyError(review_id)

        q = DBSession.query(Review.property_id, Review.user_id)
        q = q.filter(
            Review.property_id == prop_id,
            Review.user_id == user_id,
        )

        exists = DBSession.query(q.exists()).scalar()

        if not exists:
            raise KeyError(review_id)

        self.property_id = prop_id
        self.user_id = user_id
