from pyramid.view import view_config

from apartmentality.database import DBSession
from apartmentality.models.tag import Tag
from apartmentality.views import Resource, APIResource


class TagDispatcher(Resource):
    pass


@view_config(context=TagDispatcher, containment=APIResource,
             request_method="GET", renderer="api")
def api_tag_list(context, request):
    q = DBSession.query(Tag)

    return list(q.all())
