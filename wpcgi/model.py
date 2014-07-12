#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from mwoauth import mwoauth

class Template(object):
    def __init__(self, first_arg=None, form=None, **kwargs):
        if first_arg:
            raise Exception('To create a model, please use kwargs.')

        self.is_validate = False
        self.errors = {}
        self.form = form
        self.user = mwoauth.getUser()
        self.doinit(**kwargs)

    def validate(self):
        self.is_validate = True
        self.dovalidate()
        return self.errors

    def render(self, *args, **kwargs):
        self.dorender(*args, **kwargs)

    def error(self, field, m=None):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(m)

    def exists(self, page):
        path = []
        while page.exists():
            if page.isRedirectPage():
                page = page.getRedirectTarget()
                path.append(page)
            else:
                break
        else:
            return None
        return path