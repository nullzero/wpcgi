from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    from wpcgi import app
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

Base = declarative_base(cls=RepresentableBase)

class Database(object):
    def __init__(self):
        self.test = test
        
    def connect(self, url):                  
        self.engine = create_engine(name_or_url=url, convert_unicode=True)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        
    @app.teardown_appcontext
    def disconnect(self, exception=None):
        if self: # prevent calling before we connect to the database
            self.session.remove()
        if exception:
            raise exception