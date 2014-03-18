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

class ReplicatedDatabase(Database):
    def connect(self, site):      
        self.site = site
        if self.test:
            url = URL(drivername='mysql', host='localhost', database='wikidb', 
                      username='wikiuser', password='wiki_password')
        else:
            url = URL(drivername='mysql', host=site.dbName() + '.labsdb', database=site.dbName() + '_p',
                      query={'read_default_file': '~/replica.my.cnf'})
        super(ReplicatedDatabase, self).connect(url)
    
    def getpageid(self, page):
        result = self.session.query(self.get_model('page')).filter_by(
                                    page_namespace=page.namespace(),
                                    page_title=page.title(underscore=True, withNamespace=False).encode('utf-8')).first()
        if result:
            return result.page_id
        else:
            return None
    
    def toid(self, idpage):
        if isinstance(idpage, pywikibot.Page):
            idpage = self.getpageid(idpage)
        return idpage
    
    def getredirect(self, page):
        idpage = self.toid(page)
        if idpage:
            return self.session.query(self.get_model('redirect')).filter_by(rd_from=idpage).first()
        else:
            return None
    
    def getfinalid(self, page):
        seen = set()
        while True:
            idpage = self.toid(page)
            if (not idpage) or (idpage in seen):
                return None
            seen.add(idpage)
            redirect = self.getredirect(idpage)
            if redirect:
                page = pywikibot.Page(self.site, redirect.rd_title, ns=redirect.rd_namespace)
            else:
                return idpage
    
    def getlanglinks(self, frompage, tolangs=[]):
        table = self.get_model('langlinks')
        langlinks = {}
        idpage = self.getfinalid(frompage)
        if not idpage:
            return None
        args = [table.c.ll_from == idpage]
        if tolangs:
            args.append(table.c.ll_lang.in_(tolangs))
        result = self.session.query(table).filter(*args).all()
        if result:
            return {row.ll_lang: row.ll_title.decode('utf-8') for row in result}
        else:
            return {}

if __name__ == "__main__":
    enwp = ReplicatedDatabase()
    enwp.connect(pywikibot.Site())
    print enwp.getlanglinks(pywikibot.Page(pywikibot.Site(), 'B'))
    enwp.disconnect()