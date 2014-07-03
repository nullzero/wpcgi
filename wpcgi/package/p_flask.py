#!/data/project/nullzerobot/python/bin/python

from flask import *
from functools import wraps
from wpcgi.messages import msg
import flask

class _Blueprint(Blueprint):
    '''
    def __init__(self, *args, **kwargs):
        """
        This is a proof of concept of dealing with url_prefix. Must be used along with

        @app.url_value_preprocessor
        def pull_lang_code(endpoint, values):
            if values:
                g.lang_code = values.pop('lang_code', None)

        @app.url_defaults
        def add_language_code(endpoint, values):
            values.setdefault('lang_code', g.lang_code)

        """
        url_prefix = '/<lang_code>' + kwargs.pop('url_prefix', '')
        return super(_Blueprint, self).__init__(*args, url_prefix=url_prefix, **kwargs)
    '''

    def route(self, *args, **kwargs):
        methods = kwargs.pop('methods', [])
        if 'GET' not in methods:
            methods.append('GET')
        if 'POST' not in methods:
            methods.append('POST')

        return super(_Blueprint, self).route(*args, methods=methods, **kwargs)

flask.Blueprint = _Blueprint

def _render(*args, **kwargs):
    tool = kwargs.pop('tool', None)
    if tool:
        tool = tool.split('.')[-1]
    return render_template(*args, tool=tool, msg=msg, **kwargs)

flask.render = _render
render = _render # backward compat