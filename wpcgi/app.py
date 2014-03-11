#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import os
from p_flask import Flask, request, render_template, g, Blueprint
import utils
from views import frontend, dykchecker
from messages import msg
import inject

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    frontend,
    dykchecker
)

def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(config.APP_NAME)
    configure_app(app, config)
    configure_logging(app)
    configure_blueprints(app, blueprints)
    # configure_error_handlers(app)
    inject.inject(app)
    os.environ['SCRIPT_NAME'] = app.config['SCRIPT_NAME']
    return app

def configure_app(app, config):
    app.config.from_object(config)

def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def configure_logging(app):
    """Configure file logging."""

    if app.debug or app.testing:
        # skip debug and test mode.
        return

    import logging
    from logging import FileHandler

    logger = FileHandler(os.path.join(app.root_path, app.config['DEBUG_LOG']))
    logger.setLevel(logging.INFO)
    app.logger.addHandler(logger)

"""
def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500
"""