#!/data/project/nullzerobot/python/bin/python

import os
from flask.ext.script import Manager
from wpcgi import app
from config import TestConfig as Config
from wpcgi import mwoauth

app.config.from_object(Config)
mwoauth.register_mwoauth(Config)

from wpcgi.setup import setup
setup(app)

manager = Manager(app)

@manager.command
def run():
    """Run local server."""
    app.run(debug=True)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    os.system("find . -name '*.pyc' -delete")
    manager.run()