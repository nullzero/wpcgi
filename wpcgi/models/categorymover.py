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
from database.categorymover import CategoryMoverDatabase, STATUS

color = {
    STATUS.DONE_ALL: 'success',
    STATUS.DONE_FAILED: 'warning',
    STATUS.DONE_REJECTED: 'danger',
    STATUS.QUEUE_APPROVED: 'success',
    STATUS.QUEUE_WAIT: '',
}

class CategoryMover(Model):
    def doinit(self):
        self.db = CategoryMoverDatabase()
        self.db.connect('Nullzero')
        self.queue = self.db.getQueue()
        self.num_queue = len(self.queue)
        self.nav_active = {'queue': '', 'new': '', 'archive': ''}
        self.rid = None

    def setActive(self, page=None):
        for key in self.nav_active:
            self.nav_active[key] = ''
        if page in self.nav_active:
            self.nav_active[page] = 'active'

    def getQueue(self):
        self.setActive('queue')
        self.results = self.queue
        for row in self.results:
          row.color = color[row.status]

          if self.db.credit() < self.db.credit('APPROVED'):
              row.disable_approve = 'disabled'
              row.disable_reject = 'disabled'

          if row.status == STATUS.QUEUE_APPROVED:
              row.disable_approve = 'disabled'

    def getArchive(self):
        self.setActive('archive')
        self.results = self.db.getArchive()
        for row in self.results:
            row.color = color[row.status]

    def dovalidate(self):
        return True

    def save(self, rid):
        basedata = dict(
            fam = self.form.fam.data,
            lang = self.form.lang.data,
            catfrom = self.form.catfrom.data,
            catto = self.form.catto.data,
            note = self.form.note.data,
        )
        if rid:
            self.db.edit(rid, **basedata)
        else:
            self.db.new(**basedata)

    def renderEdit(self, rid=None):
        self.rid = rid
        if rid:
            self.setActive('edit')

            data = self.db.loadEdit(rid, asDict=True)
            for key in data:
                if hasattr(self.form, key):
                    getattr(self.form, key).data = data[key]
        else:
            self.setActive('new')

    def reject(self, rid):
        self.db.reject(rid)

    def approve(self, rid):
        self.db.approve(rid)
