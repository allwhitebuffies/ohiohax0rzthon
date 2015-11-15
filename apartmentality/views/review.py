from pyramid.traversal import find_interface
from pyramid.view import view_config
from sqlalchemy.orm import eagerload, defaultload
from sqlalchemy.orm.strategy_options import Load
from apartmentality.database import DBSession
from apartmentality.models.manager import Manager
from apartmentality.models.review import Review
from apartmentality.models.user import User
from apartmentality.views import Resource, APIResource
from apartmentality.views.property import PropertyResource


class ReviewDispatcher(Resource):
    def __getitem__(self, item):
        obj = ReviewResource(self.request, self, item)
        obj.__name__ = item
        return obj


class ReviewResource(Resource):
    def __init__(self, request, parent, user_id):
        self.__parent__ = parent

        try:
            user_id = int(user_id)
            property_resource = find_interface(self, PropertyResource)
            if property_resource is None:
                raise KeyError(user_id)

        except ValueError:
            raise KeyError(user_id)

        q = DBSession.query(Review.user_id)
        q = q.filter(
            Review.property_id == property_resource.property_id,
            Review.user_id == user_id,
        )

        exists = DBSession.query(q.exists())

        if not exists:
            raise KeyError(user_id)

        self.property_id = property_resource.property_id
        self.user_id = user_id


@view_config(context=ReviewDispatcher, containment=APIResource,
             request_method="GET", renderer="api")
def api_review_list(context, request):
    q = DBSession.query(Review)
    q = q.filter(
        Review.property_id == context.__parent__.property_id,
    )

    q = q.options(
        Load(Review).joinedload(Review.property),
        Load(Review).joinedload(Review.user),
        Load(Review).defaultload(Review.user).joinedload(User.person),
        Load(Review).joinedload(Review.manager),
        Load(Review).defaultload(Review.manager).joinedload(Manager.company),
        Load(Review).defaultload(Review.manager).joinedload(Manager.person),
    )

    q = q.order_by(Review.end_date.desc())

    reviews = q.all()

    return reviews


@view_config(context=ReviewResource, containment=APIResource,
             request_method="GET", renderer="api")
def api_review(context, request):
    q = DBSession.query(Review)
    q = q.filter(
        Review.property_id == context.property_id,
        Review.user_id == context.user_id,
    )

    q = q.options(
        Load(Review).joinedload(Review.property),
        Load(Review).joinedload(Review.user),
        Load(Review).defaultload(Review.user).joinedload(User.person),
        Load(Review).joinedload(Review.manager),
        Load(Review).defaultload(Review.manager).joinedload(Manager.company),
        Load(Review).defaultload(Review.manager).joinedload(Manager.person),
    )

    review = q.one()

    return review

def api_create_review(context, request):
    property_id = context.property_id
    user_id = request.cookies.get("user_id")


    q = DBSession.query(Manager)
    q = q.outerjoin(Manager.company)
    q = q.outerjoin(Manager.person)

    if name is not None:
        q = q.filter(or_(
            func.lower(Company.name).like("%%%s%%" % name.lower()),
            func.lower(Person.last_name).like("%%%s%%" % name.lower()),
            # TODO: full name search
        ))


    review = Review()
    review.property_id = property_id
