try:
    import pyrobot
except ImportError:
    import os
    import sys

    os.environ["WPROBOT_BOT"] = "Nullzerobot"
    sys.path.append("/data/project/nullzerobot/wprobot")

import wprobot
import pywikibot

from database import Database
from sqlalchemy import Column, Integer, DateTime, String, Table
import wpcgi.error
from mwoauth import mwoauth # fake mwoauth

class CREDIT(object):
    BLOCKED = -1
    ANON = 0
    USER = 1
    APPROVED = 2
    SYSOP = 3

def must_be(credit=None):
    def wrapper(fn):
        def newfn(self, *args, **kwargs):
            if getattr(CREDIT, credit) <= self.credit():
                return fn(self, *args, **kwargs)
            else:
                raise wpcgi.error.NotApprovedError()
        return newfn
    return wrapper

class SelfDatabase(Database):
    def connect(self, user=None, cachefile='selfdb.cache', **kwargs):
        if self.test:
            dic = dict(host='localhost', database='test',
                       username='root', password='password')
        else:
            dic = dict(host='tools-db', database='s51093__tools',
                       query={'read_default_file': '~/replica.my.cnf'})

        super(SelfDatabase, self).connect(dic, cachefile=cachefile, **kwargs)

        class CategoryMover(self.base):
            __table__ = Table('category_mover', self.metadata,
                Column('rid', Integer, primary_key=True),
                Column('date', DateTime, nullable=False),
                Column('fam', String(31), nullable=False),
                Column('lang', String(7), nullable=False),
                Column('catfrom', String(255), nullable=False),
                Column('catto', String(255), nullable=False),
                Column('user', String(255), nullable=False),
                Column('status', Integer, nullable=False),
                Column('note', String(300), nullable=False),
            )

        class User(self.base):
            __table__ = Table('user', self.metadata,
                Column('uid', Integer, primary_key=True),
                Column('name', String(255), nullable=False),
                Column('credit', Integer, nullable=False),
            )

        self.CategoryMover = CategoryMover
        self.User = User

        self.metadata.create_all()

        if not user:
            user = mwoauth.get_current_user()

        if user:
            self.userinfo = self.session.query(self.User).filter_by(name=user).first()
            if not self.userinfo:
                self.session.add(self.User(name=self.userinfo, credit=CREDIT.USER))
                self.session.commit()
        else:
            self.userinfo = None


    def credit(self, level=None):
        if level:
            return getattr(CREDIT, level)

        if not hasattr(self, '_credit'):
            if self.userinfo:
                self._credit = self.userinfo.credit
            else:
                self._credit = CREDIT.ANON

        return self._credit
