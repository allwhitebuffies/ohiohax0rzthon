"""Database module
"""
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import MetaData
from zope.sqlalchemy.datamanager import ZopeTransactionExtension

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

session_factory = sessionmaker(extension=ZopeTransactionExtension())
DBSession = scoped_session(session_factory)

Base = declarative_base(metadata=metadata)


def configure_database(url):
    """Configure the database connection.

    Args:
        url (str): The URL
    """

    engine = create_engine(url)
    session_factory.configure(bind=engine)
    Base.metadata.create_all(bind=engine)


from apartmentality import models
