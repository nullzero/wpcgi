#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from utils import AttrObject
from messages import msg
import pyrobot
import pywikibot
from wp import lre
import wp

class WikiTranslator(object):
    def __init__(self, form):
        self.is_validate = False

        self.errors = {}

        self.failed = False
        self.results = []

        self.path = []

        self.form = form

    def validate(self):
        self.is_validate = True

        self.error('title', msg['wikitranslator-page-not-found'])
        return self.errors

    def render(self):
        if not self.is_validate:
            raise Exception('Must validate first')


    def error(self, field, m):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(m)