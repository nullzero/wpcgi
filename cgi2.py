#!/data/project/nullzerobot/python/bin/python
import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wsgiref.handlers import CGIHandler
from wpcgi import create_app
app = create_app()
#from app2 import app

import logging
from logging.handlers import FileHandler
applogger = app.logger
file_handler = FileHandler("error.log")
file_handler.setLevel(logging.DEBUG)

applogger.setLevel(logging.DEBUG)
applogger.addHandler(file_handler)

CGIHandler().run(app)