from pyramid.view import view_config
from sqlalchemy.orm.strategy_options import Load
from sqlalchemy.sql.expression import or_
from sqlalchemy.sql.functions import func

from apartmentality.database import DBSession
from apartmentality.models.company import Company
from apartmentality.models.manager import Manager
from apartmentality.models.person import Person
from apartmentality.views import Resource, APIResource


class ManagerDispatcher(Resource):
    def __getitem__(self, item):
        obj = ManagerResource(self.request, item)
        obj.__name__ = item
        obj.__parent__ = self
        return obj


class ManagerResource(Resource):
    def __init__(self, request, manager_id):

        try:
            manager_id = int(manager_id)
        except ValueError:
            raise KeyError(manager_id)

        q = DBSession.query(Manager.id)
        q = q.filter(Manager.id == manager_id)

        exists = DBSession.query(q.exists()).scalar()

        if not exists:
            raise KeyError(manager_id)

        self.manager_id = manager_id


@view_config(context=ManagerDispatcher, containment=APIResource,
             request_method="GET", renderer="api")
def api_manager_list(context, request):
    name = request.GET.get("name")

    q = DBSession.query(Manager)

    q = q.outerjoin(Manager.company)
    q = q.outerjoin(Manager.person)

    if name is not None:
        q = q.filter(or_(
            func.lower(Company.name).like("%%%s%%" % name.lower()),
            func.lower(Person.last_name).like("%%%s%%" % name.lower()),
            # TODO: full name search
        ))

    q = q.options(
        Load(Manager).contains_eager(Manager.company),
        Load(Manager).contains_eager(Manager.person),
    )

    return list(q.all())


@view_config(context=ManagerResource, containment=APIResource,
             request_method="GET", renderer="api")
def api_manager(context, request):
    q = DBSession.query(Manager)
    q = q.filter(Manager.id == context.manager_id)
    q = q.options(
        Load(Manager).joinedload(Manager.company),
        Load(Manager).joinedload(Manager.person),
    )

    manager = q.one()

    return manager
