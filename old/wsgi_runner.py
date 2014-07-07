#!/data/project/nullzerobot/python/bin/python
import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wpcgi import app
from config import TestProductionConfig as Config

app.config.from_object(Config)

from wpcgi.setup import setup
setup(app)
#from app2 import app

from wsgiref.handlers import CGIHandler
CGIHandler().run(app)