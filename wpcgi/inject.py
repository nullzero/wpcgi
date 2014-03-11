#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from p_flask import g, request, after_this_request
from messages import msg
import time

def inject(app):
    inject_variables(app)
    inject_methods(app)
    inject_hooks(app)

def inject_variables(app):
    @app.context_processor
    def func():
        languages = {k: msg.messages[k]["__NAME__"]
                     for k in msg.messages if k is not 'msg'}

        return dict(languages=languages)

def inject_methods(app):
    def render_helper(field, errors=None, **kwargs):
        clss = kwargs.pop('class', kwargs.pop('class_', None)) or ''
        clss += ' form-control'
        if errors:
            kwargs.update({'data-toogle': 'tooltip',
		                   'data-container': 'body',
                           'data-html': 'true',
                           'title': '<ul style="padding-left: 15px;">\n' +
                                    ''.join(map(lambda x: '<li>' + x + '</li>\n', errors)) +
                                    '</ul>\n'
			              })
            clss += ' error'
        return field(class_=clss, **kwargs)

    app.jinja_env.globals.update(render_helper=render_helper)

def inject_hooks(app):
    @app.before_request
    def before_request():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

        lang = request.cookies.get('uselang')
        if lang is not None:
            msg.switch_language(lang)