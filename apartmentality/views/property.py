from pyramid.view import view_config
from sqlalchemy.orm import eagerload
from sqlalchemy.orm.strategy_options import Load
from sqlalchemy.sql.functions import func
from apartmentality.database import DBSession
from apartmentality.models.manager import Manager
from apartmentality.models.property import Property
from apartmentality.views import Resource, APIResource


class PropertyDispatcher(Resource):
    def __getitem__(self, item):
        obj = PropertyResource(self.request, item)
        obj.__name__ = item
        obj.__parent__ = self
        return obj


class PropertyResource(Resource):
    def __init__(self, request, property_id):
        super().__init__(request)
        self.children = {
            "reviews": ReviewDispatcher,
        }

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


from apartmentality.views.review import ReviewDispatcher


@view_config(context=PropertyDispatcher, containment=APIResource,
             request_method="GET", renderer="api")
def api_property_search(context, request):
    street_number = request.GET.get("street_number")
    street_name = request.GET.get("street_name")
    city = request.GET.get("city")
    state = request.GET.get("state")
    zip = request.GET.get("zip")

    q = DBSession.query(Property)

    if street_number is not None:
        q = q.filter(Property.street_number == int(street_number))

    if street_name is not None:
        q = q.filter(func.lower(Property.street_name).like("%%%s%%" %
                                                           street_name.lower()))

    if city is not None:
        q = q.filter(func.lower(Property.city).like("%%%s%%" % city.lower()))

    if state is not None:
        q = q.filter(func.lower(Property.state).like("%%%s%%" % state.lower()))

    if zip is not None:
        q = q.filter(Property.zip == zip)

    return list(q.all())


@view_config(context=PropertyResource, containment=APIResource,
             request_method="GET", renderer="api")
def api_property(context, request):
    q = DBSession.query(Property)
    q = q.filter(Property.id == context.property_id)

    property = q.one()

    return property
