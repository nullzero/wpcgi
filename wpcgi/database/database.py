from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import pickle
import os

try:
    from wpcgi import app
    from p_flask import g
    from utils import profile, debug
except ImportError:
    withoutEngine = True
    if 'WPCGI_DATABASE' in os.environ:
        test = False
    else:
        test = True
else:
    withoutEngine = False
    test = app.config['TESTING']

class RepresentableBase(object):
    def __repr__(self):
        pkeys = self.__mapper__.primary_key
        items = [(_.name, getattr(self, _.name))
                 for _ in pkeys]
        return "{0}({1})".format(
            self.__class__.__name__,
            ', '.join(['{0}={1!r}'.format(*_) for _ in items]))

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])

def asDict(fn):
    def newfn(*args, **kwargs):
        asDict = kwargs.pop('asDict', False)
        result = fn(*args, **kwargs)
        if asDict:
            result = {c.name: getattr(result, c.name)
                              for c in result.__table__.columns}
        return result
    return newfn

class Database(object):
    def __init__(self, drop=False):
        self.test = test
        self.drop_test = drop

    def connect(self, dic, cachefile, autocommit=False):
        dic['drivername'] = 'mysql'
        if 'query' not in dic:
            dic['query'] = {}
        dic['query']['charset'] = 'utf8'

        if self.test:
            self.cachefile = None

        self.cachefile = cachefile
        self.engine = create_engine(name_or_url=URL(**dic), convert_unicode=True)
        if self.cachefile and not test and os.path.exists(cachefile):
            with open(self.cachefile, 'r') as cache:
                self.metadata = pickle.load(cache)
                self.metadata.bind = self.engine
        else:
            self.metadata = MetaData(bind=self.engine)

        self.base = declarative_base(cls=RepresentableBase)
        self.session = scoped_session(sessionmaker(bind=self.engine, autocommit=autocommit))

        if not withoutEngine:
            if not hasattr(g, 'sessions'):
                g.sessions = []
            g.sessions.append(self.session)

    def get_model(self, tablename, primaries=[]):
        table = Table(tablename, self.metadata, autoload=True)
        dic = dict(__table__ = table)
        if primaries:
            dic['__mapper_args__'] = {'primary_key': [getattr(table.c, key) for key in primaries]}
        return type(tablename, (self.base,), dic)

    def save(self):
        if self.cachefile and not test:
            with open(self.cachefile, 'w') as cache:
                pickle.dump(self.metadata, cache)

    def disconnect(self):
        self.session.remove() # must disconnect before drop_all
        if self.drop_test:
            self.metadata.drop_all()

if not withoutEngine:
    @app.teardown_appcontext
    def disconnect(exception=None):
        if hasattr(g, 'sessions'):
            for session in g.sessions:
                session.remove()
        if exception:
            raise exception
