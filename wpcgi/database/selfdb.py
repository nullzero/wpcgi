from database import Database
from sqlalchemy import Column, Integer, DateTime, String, Table, Text
import wpcgi.errors
from mwoauth import mwoauth # fake mwoauth

class CREDIT(object):
    BLOCKED = -1
    ANON = 0
    USER = 1
    APPROVED = 2
    SYSOP = 3

class SelfDatabase(Database):
    def connect(self, user=None, cachefile='selfdb.cache', **kwargs):
        if self.test:
            dic = dict(host='localhost', database='test',
                       username='root', password='password')
        else:
            dic = dict(host='tools-db', database='s51093__tools',
                       query={'read_default_file': '~/replica.my.cnf'})

        super(SelfDatabase, self).connect(dic, cachefile=cachefile, **kwargs)

        class LetsTranslate(self.base):
            __table__ = Table('tool.letstranslate', self.metadata,
                Column('rid', Integer, primary_key=True),
                Column('date', DateTime, nullable=False),
                Column('pid', Integer, nullable=False),
                Column('lang', String(7), nullable=False),
                Column('fam', String(31), nullable=False),
                Column('ftitle', String(255), nullable=False),
                Column('title', String(255), nullable=False),
                Column('email', String(255), nullable=False),
                Column('name', String(255), nullable=False),
                Column('name2', String(255), nullable=True),
                Column('status', Integer, nullable=False),
                Column('content', Text, nullable=False),
                Column('content2', Text, nullable=True),
            )

        self.LetsTranslate = LetsTranslate

        self.metadata.create_all()
        '''
        if not user:
            user = mwoauth.get_current_user()

        if user:
            self.userinfo = self.session.query(self.User).filter_by(name=user).first()
            if not self.userinfo:
                self.session.add(self.User(name=user, credit=CREDIT.USER))
                self.session.commit()
        else:
            self.userinfo = None
        '''


    def credit(self, level=None):
        if level:
            return getattr(CREDIT, level)

        if not hasattr(self, '_credit'):
            if self.userinfo:
                self._credit = self.userinfo.credit
            else:
                self._credit = CREDIT.ANON

        return self._credit
