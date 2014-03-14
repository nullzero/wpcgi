#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
try:
    from p_flask import current_app
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
    test = current_app.config['TESTING']:

class Database(object):
    def connect(self, site=None):
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
            raise Exception('Cannot connect SQL')

    def pagesids(self, pages):
        ids_from_pages = {}
        for page in pages:
            query = 'SELECT `page_id` FROM `page` WHERE `page`.`page_namespace`={ns} AND `page`.`page_title`="{title}"'.format(
                ns=page.namespace(), title=page.title(underscore=True, withNamespace=False)
            )
            self.cur.execute(query)
            for row in self.cur.fetchall():
                ids_from_pages[page] = row[0]
        return ids_from_pages

    def langlinks(self, frompages=[], tolangs=[], mode='AND'):
        output = {}
        for page in frompages:
            id_ = self.pagesids([page])
            if not id_:
                continue
            id_ = id_[page]
            query = 'SELECT * FROM langlinks WHERE ll_from={pageid} {mode} ll_lang IN ({langs})'.format(
                pageid=id_, mode=mode, langs=','.join(map(lambda x: "'{}'".format(x), tolangs))
            )
            print query
            self.cur.execute(query)
            for row in self.cur.fetchall():
                output[(page, row[1])] = row[2]

        return output

    def disconnect(self):
        self.db.close()

if __name__ == "__main__":
    test = Database()
    test.connect()
    print test.langlinks(frompages=[wp.Page("ABBB"), wp.Page('TeSt Yep')], tolangs=['th'])
    test.disconnect()

"""
        pages_from_links = {}
        links_from_pages = {}

        ids_from_links = {}

        for id in links_from_ids:
            link = links_from_ids[id]
            ids_from_links[link] = id
            pages_from_links[link] = pywikibot.Page(pywikibot.Link(link)) # exception on empty string
            links_from_pages[pages_from_links[link]] = link

        for (page, link) in db.langlinks(pages):
            links_from_pages[page]

        medium = self.apiquery()
"""