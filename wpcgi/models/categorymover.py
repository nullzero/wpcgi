#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import cgi
from messages import msg
import pyrobot
import pywikibot
from pywikibot.data import api
from pywikibot.tools import itergroup
from wp import lre
import wp
from model import Model
from utils import AttrObject
import datetime
from database.categorymover import CategoryMoverDatabase

class CategoryMover(Model):
    def doinit(self):
        self.db = CategoryMoverDatabase()
        self.db.connect('Nullzero')
        self.queue = self.db.getQueue()
        self.num_queue = len(self.queue)
        self.nav_active = {'queue': '', 'new': '', 'archive': ''}
        self.setActive('queue')

    def setActive(self, page=None):
        for key in self.nav_active:
            self.nav_active[key] = ''
        if page in self.nav_active:
            self.nav_active[page] = 'active'

    def dovalidate(self):
        return True

    def save(self):
        basedata = dict(
            catfrom = self.form.catfrom.data,
            catto = self.form.catto.data,
            note = self.form.note.data
        )
        if self.rid:
            self.db.edit(self.rid, **basedata)
        else:
            self.db.new(**basedata)
    
    def renderEdit(self, rid=None):
        if rid:
            self.setActive('edit')
            self.rid = rid
            data = self.db.loadEdit(rid)
            for key in data:
                if hasattr(self.form, key):
                    getattr(self.form, key).data = data[key]
        else:
            self.setActive('new')
            self.rid = None

    def reject(self, rid):
        self.db.reject(rid)
    
    def approve(self, rid):
        self.db.approve(rid)