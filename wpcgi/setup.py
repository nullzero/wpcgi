#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import os
from p_flask import Flask, request, render_template, g, Blueprint
import utils
from mwoauth import mwoauth
from views import frontend, dykchecker, wikitranslator, categorymover, contribtracker
from messages import msg
import inject

__all__ = ['setup']

DEFAULT_BLUEPRINTS = (
    mwoauth.bp,
    frontend,
    dykchecker,
    wikitranslator,
    categorymover,
    contribtracker,
)

def setup(app, blueprints=None):
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    configure_logging(app)
    configure_blueprints(app, blueprints)
    # configure_error_handlers(app)
    inject.inject(app)
    os.environ['SCRIPT_NAME'] = app.config['SCRIPT_NAME']

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