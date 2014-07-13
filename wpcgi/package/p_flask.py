#!/data/project/nullzerobot/python/bin/python

import imp
from flask import *
from wpcgi.messages import msg
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

    def _loadSource(self, name):
        file = os.path.join(self._dir, name + '.py')
        if os.path.exists(file):
            return imp.load_source(file[:-3], file) # trim .py from the name (there will be a warning if .py is in name)
        else:
            return None

    def __init__(self, *args, **kwargs):
        self._dir = kwargs.pop('file', None)
        if self._dir:
            self._dir = os.path.dirname(self._dir)
            self._model = self._loadSource('model')
            self._form = self._loadSource('form')
            self._database = self._loadSource('database')

        if kwargs.pop('tool', False):
            kwargs['url_prefix'] = '/tools/' + args[0]
            kwargs['template_folder'] = 'templates'
            kwargs['static_folder'] = 'static'

        return super(_Blueprint, self).__init__(*args, **kwargs)

    @property
    def form(self):
        return self._form

    @property
    def model(self):
        return self._model

    @property
    def database(self):
        return self._database

    def route(self, *args, **kwargs):
        methods = kwargs.pop('methods', [])
        if 'GET' not in methods:
            methods.append('GET')
        if 'POST' not in methods:
            methods.append('POST')

        return super(_Blueprint, self).route(*args, methods=methods, **kwargs)

flask.Blueprint = _Blueprint

def _render(templatename, *args, **kwargs):
    tool = kwargs.pop('tool', None)
    if tool:
        tool = tool.split('.')[-1]
        templatename = tool + '/' + templatename
    return render_template(templatename, *args, tool=tool, msg=msg, **kwargs)

flask.render = _render