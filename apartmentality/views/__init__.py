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
        }


class APIResource(Resource):
    def __init__(self, request):
        super().__init__(request)
        self.children = {
            "users": UserDispatcher,
            "properties": PropertyDispatcher,
            "managers": ManagerDispatcher,
            "tags": TagDispatcher,
        }


from apartmentality.views.user import UserDispatcher
from apartmentality.views.property import PropertyDispatcher
from apartmentality.views.manager import ManagerDispatcher
from apartmentality.views.tag import TagDispatcher


@view_config(context=APIResource, request_method="GET", renderer="api")
def api_index(context, request):
    return {
        "hello": [1, 2, True, False, None, 2.3, "yay"],
        "key": {"key": "value"},
    }
