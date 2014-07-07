import flask.ext.sqlalchemy
from flask.ext.sqlalchemy import _BoundDeclarativeMeta, SQLAlchemy, _QueryProperty, Model
from sqlalchemy.ext.declarative import *

class RepresentableBase(Model):
    def __repr__(self):
        pkeys = self.__mapper__.primary_key
        items = [(_.name, getattr(self, _.name))
                 for _ in pkeys]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*_) for _ in items]))

    """
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
    """

class _SQLAlchemy(SQLAlchemy):
    def make_declarative_base(self):
        """Creates the declarative base."""
        base = declarative_base(cls=RepresentableBase, name='Model',
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base

flask.ext.sqlalchemy.SQLAlchemy = _SQLAlchemy