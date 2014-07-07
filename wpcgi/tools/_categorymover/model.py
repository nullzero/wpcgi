#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import cgi
from messages import msg
import pywikibot
from pywikibot.data import api
from pywikibot.tools import itergroup
from wp import lre
import wp
from wpcgi.model import Template
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

class Model(Template):
    def doinit(self, rid=None):
        self.db = CategoryMoverDatabase()
        self.db.connect()
        self.queue = self.db.getQueue()
        self.num_queue = len(self.queue)
        self.nav_active = {'queue': '', 'new': '', 'archive': ''}
        self.rid = rid

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

    def save(self):
        basedata = dict(
            fam = self.form.fam.data,
            lang = self.form.lang.data,
            catfrom = self.form.catfrom.data,
            catto = self.form.catto.data,
            note = self.form.note.data,
        )
        if self.rid:
            self.db.edit(self.rid, **basedata)
            return self.rid
        else:
            return self.db.new(**basedata)

    def renderEdit(self):
        if self.rid:
            self.setActive('edit')

            if not self.form.request:
                data = self.db.loadEdit(self.rid, asDict=True)
                for key in data:
                    if hasattr(self.form, key):
                        getattr(self.form, key).data = data[key]
        else:
            self.setActive('new')

    def reject(self):
        self.db.reject(self.rid)

    def approve(self):
        self.db.approve(self.rid)
