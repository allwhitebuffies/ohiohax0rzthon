from apartmentality.database import DBSession
from apartmentality.models.user import User
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

        try:
            user_id = int(user_id)
        except ValueError:
            raise KeyError(user_id)

        q = DBSession.query(User.id)
        q = q.filter(User.id == user_id)

        exists = DBSession.query(q.exists()).scalar()

        if not exists:
            raise KeyError(user_id)

        self.user_id = user_id
        