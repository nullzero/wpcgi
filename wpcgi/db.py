#!/data/project/nullzerobot/python/bin/python

from flask.ext.sqlalchemy import SQLAlchemy
from wpcgi import app

db = SQLAlchemy(app)

def asDict(result):
    """    if callable(obj):
            fn = obj
            def newfn(*args, **kwargs):
                asDict = kwargs.pop('asDict', False)
                result = fn(*args, **kwargs)
                if asDict:
                    return asDict(result)
                else:
                    return result
            return newfn
        else:
    """
    return {c.name: getattr(result, c.name)
            for c in result.__table__.columns}

import database.user