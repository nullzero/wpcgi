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

class CategoryMover(Model):
    def doinit(self):
        #self.result = [AttrObject(catid=1, catfrom='asd', catto='dsa', date='1 1 1', user='Nullzero')]
        pass

    def dovalidate(self):
        pass

    def dorender(self):
        pass