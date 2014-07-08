#!/data/project/nullzerobot/python/bin/python

from functools import wraps
from flask import request, make_response, redirect, flash, render
from messages import msg
from mwoauth import mwoauth
from utils import gourl

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

def require(fn):
    @wraps(fn)
    def new_fn(*in_args, **in_kwargs):
        if not mwoauth.user():
            return render('error/permission.html')
        return fn(*in_args, **in_kwargs)
    return new_fn