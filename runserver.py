#!/data/project/nullzero/python/bin/python

from flask.ext.script import Manager
from wpcgi import create_app

manager = Manager(create_app())
app = create_app()

@manager.command
def run():
    """Run local server."""

    app.run(debug=True)

if __name__ == "__main__":
    manager.run()