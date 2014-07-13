#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from messages import msg
import pywikibot
from model import Template
from utils import TextEngine

class Model(Template):
    def doinit(self):
        self.tabactive = self.form.tabStatus.data
        self.isActivePage = 'active'
        self.isActiveContent = ''
        if self.tabactive == 'content':
            self.isActivePage, self.isActiveContent = self.isActiveContent, self.isActivePage

        self.text = None
        self.title = self.form.title.data
        self.content = self.form.content.data

    def dovalidate(self):
        self.site = pywikibot.Site()

        if self.tabactive == 'page':
            if self.title:
                self.page = pywikibot.Page(self.site, self.title)
                path = self.exists(self.page)

                if path is None:
                    self.error('title', msg['contribtracker-page-not-found'])
                elif path:
                    self.page = path[-1]
            else:
                self.error('title', msg['validator-require'])
        else:
            if not self.content:
                self.error('content', msg['validator-require'])

    def dorender(self):
        if self.tabactive == 'page':
            self.content = self.page.get()
        self.textEngine = TextEngine()
        self.text = self.textEngine.remove(self.content)
        self.length, self.swath = self.textEngine.length(self.text)
        self.text = self.textEngine.convert(self.text)