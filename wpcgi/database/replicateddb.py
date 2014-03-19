try:
    import pyrobot
    from p_flask import g
except ImportError:
    import os
    import sys

    os.environ["WPROBOT_BOT"] = "Nullzerobot"
    sys.path.append("/data/project/nullzerobot/wprobot")

import wprobot
import pywikibot

from database import Database
from sqlalchemy.engine.url import URL
from utils import profile

class ReplicatedDatabase(Database):
    def connect(self, site, cachefile='replicateddb.cache'):
        self.site = site
        if self.test:
            url = URL(drivername='mysql', host='localhost', database='wikidb',
                      username='wikiuser', password='wiki_password')
        else:
            url = URL(drivername='mysql', host=site.dbName() + '.labsdb', database=site.dbName() + '_p',
                      query={'read_default_file': '~/replica.my.cnf'})
        super(ReplicatedDatabase, self).connect(url, cachefile)

        self.Page = self.get_model('page', primaries=['page_id'])
        self.Redirect = self.get_model('redirect', primaries=['rd_from'])
        self.Langlinks = self.get_model('langlinks', primaries=['ll_from'])

    def getpageid(self, page):
        result = self.session.query(self.Page.page_id).filter_by(
            page_namespace=page.namespace(),
            page_title=page.title(underscore=True, withNamespace=False).encode('utf-8')
        ).first()

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
            return self.session.query(self.Redirect).filter_by(rd_from=idpage).first()
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
                page = pywikibot.Page(self.site, redirect.rd_title.decode('utf-8'), ns=redirect.rd_namespace)
            else:
                return idpage

    def getlanglinks(self, frompage, tolangs=[]):
        langlinks = {}
        idpage = self.getfinalid(frompage)
        if not idpage:
            return None
        args = [self.Langlinks.ll_from == idpage]
        if tolangs:
            args.append(self.Langlinks.ll_lang.in_(tolangs))
        result = self.session.query(self.Langlinks).filter(*args).all()
        if result:
            return {row.ll_lang: row.ll_title.decode('utf-8') for row in result}
        else:
            return {}

if __name__ == "__main__":
    enwp = ReplicatedDatabase()
    enwp.connect(pywikibot.Site())
    print enwp.getlanglinks(pywikibot.Page(pywikibot.Site(), 'B'))
    enwp.disconnect()