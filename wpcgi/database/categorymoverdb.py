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
from sqlalchemy.engine.url import URL

class CategoryMoverDatabase(Database):
    def connect(self, site):
        self.site = site
        if self.test:
            url = URL(drivername='mysql', host='localhost', database='test', 
                      username='root', password='password')
        else:
            url = URL(drivername='mysql', host='___.labsdb', database='___',
                      query={'read_default_file': '~/replica.my.cnf'})
        super(CategoryMoverDatabase, self).connect(url)