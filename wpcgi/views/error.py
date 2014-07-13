#!/data/project/nullzerobot/python/bin/python

from flask import (Blueprint, render, request,
                   flash, url_for, redirect, session, abort)
from decorators import langswitch
from mwoauth import mwoauth
from messages import msg

error = Blueprint('errors', __name__)

@error.app_errorhandler(Exception)
def exception(e):
    if hasattr(e, 'msg'):
        flash(msg[e.msg], e.level)
    else:
        raise
    return redirect(url_for(e.next))