try:
    import pyrobot
except ImportError:
    import os
    import sys

    os.environ["WPROBOT_BOT"] = "Nullzerobot"
    sys.path.append("/data/project/nullzerobot/wprobot")

import wprobot
import pywikibot

from database import Database, Base, row2dict
from sqlalchemy.engine.url import URL
from sqlalchemy import Column, Integer, DateTime, String, Table
from datetime import datetime

STATUSES = {
    'qw', 'qa', 'ad', 'af', 'ar'
}

'''
    def __init__(self, date=datetime.now(), cat_from=None, cat_to=None, user=None, status='qw'):
        self.date = date
        self.cat_from = cat_from
        self.cat_to = cat_to
        self.user = user
        self.status = status
'''

class CategoryMoverDatabase(Database):
    def connect(self, cachefile='categorymoverdb.cache'):
        if self.test:
            url = URL(drivername='mysql', host='localhost', database='test',
                      username='root', password='password')
        else:
            url = URL(drivername='mysql', host='___.labsdb', database='___',
                      query={'read_default_file': '~/replica.my.cnf'})
        super(CategoryMoverDatabase, self).connect(url, cachefile)
        
        self.Queue = self.get_model('category_mover')

        self.session.add(self.Queue(date=datetime.now(), cat_from='a', cat_to='b', user='Nullzero', status='qa'))
        self.session.commit()

    def getQueue(self):
        return self.Queue.query.all()

    def reject(self, rid):
        data = self.Queue.query.filter_by(rid=rid).first()
        if not data:
            return False
        dic = row2dict(data)
        self.session.delete(data)
        self.session.commit()
        print dic

if __name__ == "__main__":
    cm = CategoryMoverDatabase()
    cm.connect()
    print cm.getQueue()

    cm.reject(1)