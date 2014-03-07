import time
from p_flask import Flask, request, render_template, g, Blueprint
import utils
from views import frontend, dykchecker
from config import Config
from messages import msg

__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    frontend,
    dykchecker
)

def create_app(config=None, app_name=None, blueprints=None):
    if app_name is None:
        app_name = Config.APP_NAME
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS
    app = Flask(app_name)
    app.config.from_object(Config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    # configure_extensions(app)
    #configure_logging(app)
    configure_template_filters(app)
    # configure_error_handlers(app)
    
    @app.context_processor
    def inject_variables():
        return dict(msg=msg, 
                    languages={k: msg.messages[k]["__NAME__"] for k in msg.messages if k is not 'msg'})
    
    def render_helper(field, errors=None, **kwargs):
        clss = kwargs.pop('class', kwargs.pop('class_', None)) or ''
        clss += ' form-control'
        if errors:
            kwargs.update({'data-toogle': 'tooltip', 
			               'data-placement': 'right', 
		                   'data-container': 'body',
                           'data-html': 'true',
                           'title': '<ul style="padding-left: 15px;">\n' + 
                                    ''.join(map(lambda x: '<li>' + x + '</li>\n', errors)) + '</ul>\n'
			              })
            clss += ' error'
        return field(class_=clss, **kwargs)
            
        return field(**dict(kwargs or {}, **(okwargs or {})))
    app.jinja_env.globals.update(render_helper=render_helper)
    
    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
        
    return app

def configure_extensions(app):
    # # sqlalchemy
    # db.init_app(app)
    # # mail
    # mail.init_app(app)
    # # cache
    # cache.init_app(app)
    # 
    # # babel
    # babel = Babel(app)
    # @babel.localeselector
    # def get_locale():
    #     accept_languages = app.config.get('ACCEPT_LANGUAGES')
    #     return request.accept_languages.best_match(accept_languages)
    # 
    # # login.
    # login_manager.login_view = 'frontend.login'
    # login_manager.refresh_view = 'frontend.reauth'
    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))
    # login_manager.setup_app(app)
    pass


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):
    @app.template_filter()
    def pretty_date(value):
        return utils.pretty_date(value)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # skip debug and test mode.
        return

    import logging
    from logging.handlers import RotatingFileHandler, SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    app.logger.setLevel(logging.INFO)

    debug_log = os.path.join(app.root_path, app.config['DEBUG_LOG'])
    file_handler = logging.handlers.RotatingFileHandler(debug_log, maxBytes=100000, backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(file_handler)

    # ADMINS = ['imwilsonxu@gmail.com']
    # mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
    #                            app.config['MAIL_USERNAME'],
    #                            ADMINS,
    #                            'O_ops... Fbone failed!',
    #                            (app.config['MAIL_USERNAME'],
    #                             app.config['MAIL_PASSWORD']))
    # mail_handler.setLevel(logging.ERROR)
    # mail_handler.setFormatter(logging.Formatter(
    #     '%(asctime)s %(levelname)s: %(message)s '
    #     '[in %(pathname)s:%(lineno)d]')
    # )
    # app.logger.addHandler(mail_handler)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(405)
    def method_not_allowed_page(error):
        return render_template("errors/method_not_allowed.html"), 405

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500