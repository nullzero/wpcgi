#!/data/project/nullzero/python/bin/python
import site
site.addsitedir("/data/project/nullzero/python/lib/python2.7/site-packages")

from wsgiref.handlers import CGIHandler
from wpcgi import create_app
app = create_app()
#from app2 import app

CGIHandler().run(app)