from pyramid.view import view_config


class Resource(object):
    """Base resource class.
    """

    def __init__(self, request):
        self.request = request
        self.children = {}

    def __getitem__(self, item):
        obj = self.children[item](self.request)
        obj.__name__ = item
        obj.__parent__ = self
        return obj


class RootResource(Resource):
    def __init__(self, request):
        super().__init__(request)
        self.children = {
            "api": APIResource,
            "users": UserDispatcher,
            "properties": PropertyDispatcher,
            "managers": ManagerDispatcher,
            "tags": TagDispatcher,
        }


class APIResource(Resource):
    def __init__(self, request):
        super().__init__(request)
        self.children = {
            "users": UserDispatcher,
            "properties": PropertyDispatcher,
            "managers": ManagerDispatcher,
            "tags": TagDispatcher,
            "photos": PhotoDispatcher,
        }


from apartmentality.views.user import UserDispatcher
from apartmentality.views.property import PropertyDispatcher
from apartmentality.views.manager import ManagerDispatcher
from apartmentality.views.tag import TagDispatcher
from apartmentality.views.photo import PhotoDispatcher


@view_config(context=RootResource, request_method="GET", renderer="index.html")
def api_index(context, request):
    return {}
