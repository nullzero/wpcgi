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
from database.letstranslate import LetsTranslateDatabase, STATUS

class LetsTranslate(Model):
    def doinit(self, rid=None, mode=None):
        self.db = LetsTranslateDatabase()
        self.db.connect()
        self.list = self.db.getList()
        self.rid = rid
        self.mode = mode

    def dovalidate(self):
        return True

    def getList(self):
        if self.mode == 'translated':
            status = STATUS.TRANSLATED
        elif self.mode == 'reserved':
            status = STATUS.RESERVED
        elif self.mode == 'final':
            status = STATUS.FINAL
        elif self.mode == 'rejected':
            status = STATUS.REJECTED
        elif self.mode == 'done':
            status = STATUS.DONE

        self.results = filter(lambda x: x.status == status, self.list)

    def renderEdit(self):
        if self.mode != 'new' and not self.form.request:
            data = self.db.loadEdit(self.rid, asDict=True)
            for key in data:
                if hasattr(self.form, key):
                    getattr(self.form, key).data = data[key]

    def save(self):
        wikify = None
        basedata = {}
        fieldlist = []

        if self.mode == 'new':
            fieldlist = ['pid', 'name', 'lang', 'fam', 'title', 'ftitle', 'content', 'email']
            if self.form.wikiuser.data:
                wikify = 'name'
        elif self.mode == 'translated':
            fieldlist = ['name2']
            if self.form.wikiuser.data:
                wikify = 'name2'
            basedata['status'] = STATUS.RESERVED
        elif self.mode == 'reserved':
            fieldlist = ['title', 'content2']
            basedata['status'] = STATUS.FINAL
        elif self.mode == 'final':
            fieldlist = ['title', 'content2']
            basedata['status'] = STATUS.DONE

        for field in fieldlist:
            basedata[field] = getattr(self.form, field).data

        if wikify:
            basedata[wikify] = u'[[User:{}]]'.format(basedata[wikify])

        # return for what?
        if self.rid:
            self.db.edit(self.rid, **basedata)
            return self.rid
        else:
            return self.db.new(**basedata)

    def reject(self):
        self.db.reject(self.rid)

    def recover(self):
        self.db.recover(self.rid)
