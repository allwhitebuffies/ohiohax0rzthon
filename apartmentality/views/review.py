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

        # TODO: check review id exists
        self.review_id = None
