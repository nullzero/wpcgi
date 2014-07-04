#!/data/project/nullzerobot/python/bin/python

import imp
from flask import *
from functools import wraps
from wpcgi.messages import msg
import wpcgi.messages
import flask
import os

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

    def __init__(self, *args, **kwargs):
        if kwargs.pop('tool', False):
            self.tool = args[0]
            kwargs['url_prefix'] = '/tools/' + args[0]
            kwargs['template_folder'] = 'templates'
        else:
            self.tool = None
        return super(_Blueprint, self).__init__(*args, **kwargs)

    def route(self, *args, **kwargs):
        methods = kwargs.pop('methods', [])
        if 'GET' not in methods:
            methods.append('GET')
        if 'POST' not in methods:
            methods.append('POST')

        return super(_Blueprint, self).route(*args, methods=methods, **kwargs)

    def form(self, *args, **kwargs):
        form = imp.load_source('form', os.path.join(os.path.dirname(wpcgi.messages.__file__), 'tools', self.tool, 'form.py'))
        return form.form(*args, **kwargs)



flask.Blueprint = _Blueprint

def _render(*args, **kwargs):
    tool = kwargs.pop('tool', None)
    if tool:
        tool = tool.split('.')[-1]
    return render_template(*args, tool=tool, msg=msg, **kwargs)

flask.render = _render
