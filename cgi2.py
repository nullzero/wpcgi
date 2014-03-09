#!/data/project/nullzerobot/python/bin/python
import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wsgiref.handlers import CGIHandler
from wpcgi import create_app
from config import ProductionConfig as Config

app = create_app(Config)
#from app2 import app

CGIHandler().run(app)