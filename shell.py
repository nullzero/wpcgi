import os
import readline
from pprint import pprint

from wpcgi import app
import config
app.config.from_object(config.TestConfig)
from wpcgi.setup import setup
setup(app)

from wpcgi.db import db
import wpcgi.database.user as model

os.environ['PYTHONINSPECT'] = 'True'