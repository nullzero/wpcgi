#!/data/project/nullzerobot/python/bin/python

import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wpcgi import app
from config import ProductionConfig as Config
app.config.from_object(Config)

from wpcgi.setup import setup
setup(app, Config)

from flup.server.fcgi import WSGIServer
if __name__ == '__main__':
    WSGIServer(app).run()