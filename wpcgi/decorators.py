#!/data/project/nullzerobot/python/bin/python

from functools import wraps
from flask import request, make_response, redirect, flash, render
from messages import msg
from utils import gourl
import wpcgi.errors
from mwoauth import mwoauth

def langswitch(fn):
    """
    Deal with ?uselang=...
    """
    @wraps(fn)
    def new_fn(*in_args, **in_kwargs):
        lang = request.args.get('uselang', None)
        setcookie = (lang and msg.switch_language(lang))
        response = make_response(fn(*in_args, **in_kwargs))
        if setcookie:
            response.set_cookie('uselang', lang)
        return response
    return new_fn

def in_group(groups, error=False):
    def decorator(fn):
        @wraps(fn)
        def callee(*args, **kwargs):
            user = mwoauth.getUser()
            if not user.in_group(groups):
                if error:
                    raise wpcgi.errors.NotApprovedError()
                return render('errors/permission.html', groups=groups)
            else:
                return fn(*args, **kwargs)
        return callee
    return decorator