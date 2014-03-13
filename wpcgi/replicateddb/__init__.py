#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

#import MySQLdb

class Database(object):
    """
    def connect(self, site):
        try:
            self.db = MySQLdb.connect(host=site.dbName() + '.labsdb',
                                      db=site.dbName() + '_p',
                                      read_default_file="~/replica.my.cnf")
            self.cur = self.db.cursor()
        except:
            pass
        finally:
            self.db.close()
    """

    def __init__(self):
        class Something(object):
            def execute(self, o):
                print 'execute: ', o

            def fetchall(self):
                return [(0, 1, 2), (2, 3, 4)]

        self.cur = Something()

    def pagesids(self, pages):
        pass

    def langlinks(self, frompages=[], tolangs=[], mode='AND'):
        query = 'SELECT * FROM langlinks WHERE '
        conditions = []
        pageids = self.pageids(frompages)
        if pageids:
            conditions.append('ll_from IN ' + self.totuple(pageids.values()))
        if tolangs:
            conditions.append('ll_lang IN ' + self.totuple(tolangs))

        query += (' {} '.format(mode)).join(conditions)

        self.cur.execute(query)
        data = cur.fetchall()
        map_pageid_data = {}
        for row in data:
            map_pageid_data[row[0]] = (row[1], row[2])
        output = {}
        for i, page in enumerate(frompages):
            if page in pagesids and pagesids[page] in map_pageid_data:
                output[page] = map_pageid_data[pagesids[page]]
        return output

    """"
    def disconnect(self):
        self.db.close()
    """
if __name__ == "__main__":
    test = Database()
    test.langlinks()

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
