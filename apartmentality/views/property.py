from apartmentality.database import DBSession
from apartmentality.models.property import Property
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

        try:
            id_int = int(property_id)
        except ValueError:
            raise KeyError(property_id)

        q = DBSession.query(Property.id)
        q = q.filter(Property.id == id_int)

        exists = DBSession.query(q.exists()).scalar()

        if not exists:
            raise KeyError(property_id)

        self.property_id = id_int