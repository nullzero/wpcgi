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
        pass

    def setActive(self, page):
        for key in self.nav_active:
            self.nav_active[key] = ''
        self.nav_active[page] = 'active'

    def dovalidate(self):
        pass

    def dorender(self):
        pass

    def renderQueue(self):
        # self.db.new('A', 'B', 'Change Category from A to B')
        # self.db.new('A', 'B', 'Change Category from A to B')
        # self.db.new('A', 'B', 'Change Category from A to B')
        # self.db.commit()
        self.setActive('queue')
        self.result = self.db.getQueue()
        # self.db.disconnect() # For test

    def renderReject(self, rid):
        self.db.reject(rid)