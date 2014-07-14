#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint
from decorators import langswitch
from mwoauth import mwoauth
from messages import msg

error = Blueprint('errors', __name__)

@error.app_errorhandler(Exception)
@langswitch
def exception(e):
    if hasattr(e, 'next'):
        return e.next()
    else:
        raise

@error.app_errorhandler(404)
@langswitch
def error404(e):
    return render('errors/404.html', url=gourl())
