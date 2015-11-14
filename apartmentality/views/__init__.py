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

        }


class APIResource(Resource):
    def __init__(self, request):
        super().__init__(request)
        self.children = {
        }
