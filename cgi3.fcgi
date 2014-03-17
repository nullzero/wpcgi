#!/data/project/nullzerobot/python/bin/python

from flup.server.fcgi import WSGIServer
import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wpcgi import app
from config import ProductionConfig as Config
from wpcgi.setup import setup
setup(app, Config)

if __name__ == '__main__':
    WSGIServer(app).run()