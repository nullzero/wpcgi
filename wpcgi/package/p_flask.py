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
        self._model = None
        self._form = None
        self._database = None

        self._dir = kwargs.pop('file', None)
        if self._dir:
            self._dir = os.path.dirname(self._dir)

        if kwargs.pop('tool', False):
            kwargs['url_prefix'] = '/tools/' + args[0]
            kwargs['template_folder'] = 'templates'

        return super(_Blueprint, self).__init__(*args, **kwargs)

    def route(self, *args, **kwargs):
        methods = kwargs.pop('methods', [])
        if 'GET' not in methods:
            methods.append('GET')
        if 'POST' not in methods:
            methods.append('POST')

        return super(_Blueprint, self).route(*args, methods=methods, **kwargs)

    @property
    def form(self):
        if self._form:
            return self._form
        self._form = imp.load_source('form', os.path.join(self._dir, 'form.py'))
        return self._form

    @property
    def model(self):
        if self._model:
            return self._model
        self._model = imp.load_source('model', os.path.join(self._dir, 'model.py'))
        return self._model

    @property
    def database(self):
        if self._database:
            return self._database
        self._database = imp.load_source('model', os.path.join(self._dir, 'database.py'))
        return self._database

flask.Blueprint = _Blueprint

def _render(*args, **kwargs):
    tool = kwargs.pop('tool', None)
    if tool:
        tool = tool.split('.')[-1]
    return render_template(*args, tool=tool, msg=msg, **kwargs)

flask.render = _render
