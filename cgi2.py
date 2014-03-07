#!/data/project/nullzero/python/bin/python
import site
site.addsitedir("/data/project/nullzero/python/lib/python2.7/site-packages")

from wsgiref.handlers import CGIHandler
from wpcgi import create_app

app = create_app()

import logging
from logging import FileHandler
logger = FileHandler('error.log')
logger.setLevel(logging.DEBUG)
app.logger.addHandler(logger)
CGIHandler().run(app)