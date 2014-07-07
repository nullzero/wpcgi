#!/data/project/nullzerobot/python/bin/python

from flask.ext.sqlalchemy import SQLAlchemy
from wpcgi import app

db = SQLAlchemy(app)