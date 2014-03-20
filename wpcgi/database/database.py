from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pickle
import os

try:
    from wpcgi import app
    from p_flask import g
    from utils import profile, debug
except ImportError:
    print ">>> Enter test mode"
    test = True

    class Dummy(object):
        def teardown_appcontext(self, fn):
            def newfn(*args, **kwargs):
                return fn(*args, **kwargs)
            return newfn

    app = Dummy()
else:
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

class Database(object):
    def __init__(self):
        self.test = test

    def connect(self, url, cachefile):
        self.cachefile = cachefile
        self.engine = create_engine(name_or_url=url, convert_unicode=True)
        if not test and os.path.exists(cachefile):
            with open(self.cachefile, 'r') as cache:
                self.metadata = pickle.load(cache)
                self.metadata.bind = self.engine
        else:
            self.metadata = MetaData(bind=self.engine)

        self.base = declarative_base(cls=RepresentableBase)
        self.session = scoped_session(sessionmaker(bind=self.engine))

        if not test:
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
        if not test:
            with open(self.cachefile, 'w') as cache:
                pickle.dump(self.metadata, cache)

    def disconnect(self):
        self.session.remove()

row2dict = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}

@app.teardown_appcontext
def disconnect(exception=None):
    if hasattr(g, 'sessions'):
        for session in g.sessions:
            session.remove()
    if exception:
        raise exception