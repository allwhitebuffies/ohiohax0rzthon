from pyramid.view import view_config
from sqlalchemy.orm import eagerload
from sqlalchemy.orm.strategy_options import Load
from sqlalchemy.sql.functions import func
from apartmentality.database import DBSession
from apartmentality.models.manager import Manager
from apartmentality.models.property import Property
from apartmentality.models.review import Review
from apartmentality.models.tag import Tag
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


from apartmentality.views.review import ReviewDispatcher, api_review_list


@view_config(context=PropertyDispatcher, containment=APIResource,
             request_method="GET", renderer="api")
def api_property_search(context, request):
    street_number = request.GET.get("street_number")
    street_name = request.GET.get("street_name")
    city = request.GET.get("city")
    state = request.GET.get("state")
    zip = request.GET.get("zip")

    q = DBSession.query(Property, func.avg(Review.rating_average))

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

    q = q.outerjoin(Property.reviews)
    q = q.group_by(Property.id)

    q = q.limit(7)

    results = []

    for property, avg in q.all():
        if avg is not None:
            property.overall = int(avg)
        else:
            property.overall = None
        results.append(property)

    return results


@view_config(context=PropertyDispatcher, request_method="GET",
             renderer="listings.html")
def html_property_search(context, request):
    data = api_property_search(context, request)

    return {"results": data}


@view_config(context=PropertyDispatcher, containment=APIResource,
             request_method="POST", renderer="api")
def api_create_property(context, request):
    street_info = request.json_body.get("address")
    city = request.json_body.get("city")
    state = request.json_body.get("state")
    zip = request.json_body.get("zip")

    num, sep, street = street_info.partition(" ")

    property = Property()
    property.street_number = int(num)
    property.street_name = street
    property.city = city
    property.state = state
    property.zip = int(zip)

    DBSession.add(property)
    DBSession.flush()

    return property


@view_config(context=PropertyResource, containment=APIResource,
             request_method="GET", renderer="api")
def api_property(context, request):
    q = DBSession.query(Property)
    q = q.filter(Property.id == context.property_id)

    property = q.one()

    q = DBSession.query(Tag.text, func.count(Tag.id))
    q = q.select_from(Review)
    q = q.join(Review.tags)
    q = q.filter(Review.property_id == property.id)
    q = q.group_by(Tag.id)
    q = q.order_by(func.count(Tag.id).desc())
    q = q.limit(5)

    property.top_tags = {r[0]: r[1] for r in q.all()}

    return property


@view_config(context=PropertyResource, request_method="GET",
             renderer="reviews.html")
def html_property(context, request):
    dispatcher = ReviewDispatcher(request)
    dispatcher.__name__ = "reviews"
    dispatcher.__parent__ = context

    return {
        "property": api_property(context, request),
        "reviews": api_review_list(dispatcher, request),
        "photo": "/img/house-%d.jpg" % (context.property_id % 10),
    }
