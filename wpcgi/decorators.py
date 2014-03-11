#!/data/project/nullzerobot/python/bin/python

from functools import wraps
from p_flask import request, make_response
from messages import msg

def langswitch(fn):
    """
    Deal with ?uselang=...
    """
    @wraps(fn)
    def new_fn(*in_arg, **in_kwargs):
        lang = request.args.get('uselang', None)
        setcookie = (lang and msg.switch_language(lang))
        response = make_response(fn(*in_arg, **in_kwargs))
        if setcookie:
            response.set_cookie('uselang', lang)
        return response
    return new_fn
