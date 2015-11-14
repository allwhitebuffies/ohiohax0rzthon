from apartmentality.views import Resource


class PropertyDispatcher(Resource):
    def __getitem__(self, item):
        obj = PropertyResource(self.request, item)
        obj.__name__ = item
        obj.__parent__ = self
        return obj


class PropertyResource(Resource):
    def __init__(self, request, property_id):
        super().__init__(request)

        # TODO: get property_id

        self.property_id = None
