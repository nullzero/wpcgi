#!/data/project/nullzerobot/python/bin/python
import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wsgiref.handlers import CGIHandler
from wpcgi import app
from config import TestProductionConfig as Config
from wpcgi.setup import setup 
setup(app, Config)
#from app2 import app

CGIHandler().run(app)