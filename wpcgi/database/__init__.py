'''
#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

try:
    from wpcgi import app
except ImportError:
    test = True
    import os
    import sys

    os.environ["WPROBOT_BOT"] = "Nullzerobot"
    sys.path.append("/data/project/nullzerobot/wprobot")

    import wprobot
    import wp
    import pywikibot
else:
    import pywikibot
    test = app.config['TESTING']        
            

class Database(object):
    def connect(self, site=None):
        self.site = site
        try:
            if test:
                self.db = MySQLdb.connect(host='localhost',
                                          db='wikidb',
                                          user='wikiuser',
                                          passwd='wiki_password')
            else:
                self.db = MySQLdb.connect(host=site.dbName() + '.labsdb',
                                          db=site.dbName() + '_p',
                                          read_default_file="~/replica.my.cnf")
            self.cur = self.db.cursor()
        except:
            self.db.close()
            raise

    def pagesids(self, pages, single=False):
        """
        @type pages: list of pywikibot.Page
        """
        ids_from_pages = {}
        for page in pages:
            query = ('SELECT `page_id` '
                     'FROM `page` '
                     'WHERE `page`.`page_namespace`=%s AND '
                           '`page`.`page_title`=%s')
            self.cur.execute(
                query,
                (
                    page.namespace(),
                    self.db.escape_string(page.title(underscore=True, withNamespace=False).encode('utf-8'))
                )
            )
            for row in self.cur.fetchall():
                ids_from_pages[page] = row[0]
        if single:
            if ids_from_pages:
                return ids_from_pages.values()[0]
            else:
                return None
        return ids_from_pages

    def redirects(self, pages, single=False):
        """
        @type frompages: list of pywikibot.Page or list of int
        """
        output = {}
        for page in pages:
            if isinstance(page, pywikibot.Page):
                id_page = self.pageids([page], single=True)
                if not id_page:
                    continue
            else:
                id_page = page

            query = ('SELECT * '
                     'FROM `redirect` '
                     'WHERE `redirect`.`rd_from`=%s')

            self.cur.execute(
                query,
                (id_page,)
            )

            for row in self.cur.fetchall():
                output[page] = (row[1], row[2])

        if single:
            if output:
                return output.values()[0]
            else:
                return None
        return output

    def get_final_id(self, page):
        seen = set()
        while True:
            if isinstance(page, pywikibot.Page):
                id_page = self.pagesids([page], single=True)
                if not id_page:
                    return None
            else:
                id_page = page

            if id_page in seen:
                # circular redirect
                # TODO: how to handle it?
                return None
            seen.add(id_page)
            page_redirect = self.redirects([id_page], single=True)
            if page_redirect:
                page = pywikibot.Page(self.site, page_redirect[1], ns=page_redirect[0])
            else:
                return id_page

    def langlinks(self, frompages=[], tolangs=[], mode='AND'):
        """
        @type frompages: list of pywikibot.Page
        """

        output = {}
        for page in frompages:
            id_page = self.get_final_id(page)
            if not id_page:
                continue

            query = ('SELECT * '
                     'FROM langlinks '
                     'WHERE ll_from=%s {mode} ').format(mode=mode)

            if tolangs:
                query += ('ll_lang IN ({langs})').format(
                    langs=','.join(map(lambda x: "'{}'".format(x), tolangs))
                )

            self.cur.execute(
                query,
                (id_page,)
            )

            for row in self.cur.fetchall():
                output[(page, row[1])] = row[2].decode('utf-8')

        return output

    def disconnect(self):
        self.db.close()

if __name__ == "__main__":
    test = Database()
    test.connect()
    print test.langlinks(frompages=[wp.Page("ABBB"), wp.Page('TeSt Yep')], tolangs=['th'])
    test.disconnect()
    
    
    

        else:
            if test:
                url = URL(drivername='mysql', host='localhost', database='test', 
                          username='root', password='password')
            else:
                url = URL(drivername='mysql', host=site.dbName() + '.labsdb', database=site.dbName() + '_p',
                          query={'read_default_file': '~/replica.my.cnf'})
'''