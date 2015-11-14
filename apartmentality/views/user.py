from apartmentality.views import Resource


class UserDispatcher(Resource):
    def __init__(self, request):
        super().__init__(request)

    def __getitem__(self, item):
        user = UserResource(self.request, item)
        user.__name__ = item
        user.__parent__ = self
        return user


class UserResource(Resource):
    def __init__(self, request, user_id):
        super().__init__(request)

        # TODO: test if user exists
        self.user_id = None
