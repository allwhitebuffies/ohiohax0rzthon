from pyramid.httpexceptions import HTTPSeeOther
from pyramid.view import view_config

from apartmentality.database import DBSession
from apartmentality.models.photo import Photo
from apartmentality.views import Resource, APIResource


class PhotoDispatcher(Resource):
    def __getitem__(self, item):
        obj = PhotoResource(self.request, item)
        obj.__name__ = item
        obj.__parent__ = self
        return obj


class PhotoResource(Resource):
    def __init__(self, request, photo_id):
        self.photo_id = photo_id


@view_config(context=PhotoResource, containment=APIResource,
             request_method="GET")
def api_photo(context, request):
    q = DBSession.query(Photo)
    q = q.filter(Photo.id == context.photo_id)

    photo = q.scalar()

    return HTTPSeeOther(location=photo.url)
