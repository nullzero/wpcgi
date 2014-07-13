import os
import readline
from pprint import pprint

from wpcgi import app
import config

used_config = None
while True:
    used_config = raw_input('Please enter a configuration: ')
    if used_config in ['TestConfig', 'ProductionConfig']:
        break
app.config.from_object(getattr(config, used_config))
from wpcgi.setup import setup
setup(app)

from wpcgi.db import db
import wpcgi.database.user as user_model

os.environ['PYTHONINSPECT'] = 'True'