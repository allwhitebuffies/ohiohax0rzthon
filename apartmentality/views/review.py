import datetime

from pyramid.traversal import find_interface
from pyramid.view import view_config
from sqlalchemy.orm import eagerload, defaultload
from sqlalchemy.orm.strategy_options import Load
from sqlalchemy.sql.functions import func

from apartmentality.database import DBSession
from apartmentality.models.manager import Manager
from apartmentality.models.review import Review
from apartmentality.models.tag import Tag
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
        Load(Review).subqueryload(Review.tags),
    )

    review = q.one()

    return review


@view_config(context=ReviewDispatcher, containment=APIResource,
             request_method="POST", renderer="api")
def api_create_review(context, request):
    property_id = context.property_id
    user_id = request.cookies.get("user_id")

    manager = request.json_body.get("manager")
    rating_kitchen = request.json_body.get("rating_kitchen")
    rating_bedroom = request.json_body.get("rating_bedroom")
    rating_bathroom = request.json_body.get("rating_bathroom")
    rating_area = request.json_body.get("rating_area")
    rent = request.json_body.get("rent")
    tag_ids = request.json_body.get("tags")

    avg_sum = 0
    avg_total = 0

    if rating_kitchen is not None:
        avg_sum += rating_kitchen
        avg_total += 1
    if rating_bedroom is not None:
        avg_sum += rating_bedroom
        avg_total += 1
    if rating_bathroom is not None:
        avg_sum += rating_bathroom
        avg_total += 1
    if rating_area is not None:
        avg_sum += rating_area
        avg_total += 1

    if avg_total > 0:
        rating_avg = avg_sum / avg_total
    else:
        rating_avg = None

    text = request.json_body.get("text")

    q = DBSession.query(Manager)
    q = q.filter(func.lower(Manager.name).like("%%%s%%" % manager.lower()))

    manager = q.scalar()

    if manager is None:
        manager = Manager()
        manager.name = manager
        DBSession.add(manager)
        DBSession.flush()

    review = Review()
    review.user_id = user_id
    review.property_id = property_id
    review.manager = manager
    review.rating_kitchen = rating_kitchen
    review.rating_bathroom = rating_bathroom
    review.rating_area = rating_area
    review.rating_average = rating_avg

    review.rent = rent

    review.text = text
    review.date = datetime.datetime.now()

    for tag_id in tag_ids:
        q = DBSession.query(Tag)
        q = q.filter(Tag.id == tag_id)
        tag = q.scalar()

        if tag is not None:
            review.tags.append(tag)

    DBSession.add(review)
    DBSession.flush()

    return {}
