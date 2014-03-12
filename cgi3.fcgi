#!/data/project/nullzerobot/python/bin/python

from flup.server.fcgi import WSGIServer
import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

from wpcgi import create_app
from config import ProductionConfig as Config

app = create_app(Config)

if __name__ == '__main__':
    WSGIServer(app).run()