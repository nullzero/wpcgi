#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from p_flask import g, request, after_this_request
from messages import msg
import time
from mwoauth import mwoauth
import c

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
        tooltip = kwargs.pop('tooltip', '')
        clss += ' form-control'
        if errors or tooltip:
            errorsmsg = ''
            if errors:
                errorsmsg += msg['core-error'] + '\n'
                errorsmsg += '<ul class="error-tooltip">\n'
                errorsmsg += ''.join(map(lambda x: '<li>' + x + '</li>\n', errors))
                errorsmsg += '</ul>\n'
            if errors and tooltip:
                tooltip += '<hr>\n'
            kwargs.update({'data-toogle': 'tooltip',
                           'data-container': 'body',
                           'data-html': 'true',
                           'title': tooltip + errorsmsg
                          })
            clss += ' error'
        return field(class_=clss, **kwargs)

    class User(object):
        def __init__(self):
            self.login = False

    user = User()

    app.jinja_env.globals.update(render_helper=render_helper,
                                 msg=msg,
                                 user=user,
                                 mwoauth=mwoauth,
                                 str=str,
                                 c=c)


def inject_hooks(app):
    @app.before_request
    def before_request():
        g.debugtext = ""
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

        '''
        lang = request.cookies.get('uselang')
        if lang is not None:
            msg.switch_language(lang)
        '''
