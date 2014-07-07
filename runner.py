#!/data/project/nullzerobot/python/bin/python

import site
site.addsitedir("/data/project/nullzerobot/python/lib/python2.7/site-packages")

import os
from flask.ext.script import Manager
from flask.ext.script.commands import Clean
from wpcgi import app

SQLALCHEMY_DATABASE_URI = None
SQLALCHEMY_MIGRATE_REPO = None

def create_app(config=None):
    import config as config_mod
    app.config.from_object(getattr(config_mod, config))
    global SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
    SQLALCHEMY_DATABASE_URI = app.config['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_MIGRATE_REPO = app.config['SQLALCHEMY_MIGRATE_REPO']
    from wpcgi.setup import setup
    setup(app)
    return app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=True, help='config file')
manager.add_command('clean', Clean())

@manager.command
def run():
    """Run local server."""
    if app.config['MODE'] == 'production':
        from flup.server.fcgi import WSGIServer
        WSGIServer(app).run()
    else:
        app.run(debug=True)

@manager.command
def db_create():
    """Create database."""
    from migrate.versioning import api
    from wpcgi.db import db
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

@manager.command
def db_migrate():
    import imp
    from migrate.versioning import api
    from wpcgi.db import db
    migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%04d_migration.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
    open(migration, "wt").write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

@manager.command
def db_upgrade():
    from migrate.versioning import api
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

def db_downgrade():
    from migrate.versioning import api
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
    print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

if __name__ == "__main__":
    manager.run()
