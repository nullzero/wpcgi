#!/data/project/nullzerobot/python/bin/python

import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wpcgi import app
from config import ProductionConfig as Config
from wpcgi import mwoauth

app.config.from_object(Config)
mwoauth.register_mwoauth(Config)

from wpcgi.setup import setup
setup(app)

from flup.server.fcgi import WSGIServer
if __name__ == '__main__':
    WSGIServer(app).run()