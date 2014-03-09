#!/data/project/nullzerobot/python/bin/python

from flask.ext.script import Manager
from wpcgi import create_app
from config import TestConfig as Config

app = create_app(Config)
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
    manager.run()