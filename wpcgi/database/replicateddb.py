try:
    import pyrobot
    from p_flask import g
    from utils import profile
except ImportError:
    import os
    import sys

    os.environ["WPROBOT_BOT"] = "Nullzerobot"
    sys.path.append("/data/project/nullzerobot/wprobot")

import wprobot
import pywikibot

from database import Database
from sqlalchemy.engine.url import URL
from collections import defaultdict

"""
get... = map input to output | getlanglinks
"""

def sort_inputs_by_ns(inputs):
    groups = defaultdict(list)
    for page in sorted(inputs, key=lambda page: page.namespace()):
        groups[page.namespace()].append(page)
    return groups

def separate_ns(fn):
    def new_fun(self, *args, **kwargs):
        inputs = kwargs.pop('inputs')
        sort_by_ns = kwargs.pop('sort_by_ns', None)
        if ((hasattr(self, 'internal_call') and sort_by_ns is None) or (inputs and not isinstance(inputs[0], pywikibot.Page))):
            sort_by_ns = False
        else:
            self.internal_call = True

        if sort_by_ns or (sort_by_ns is None):
            old = fn(self, *args, inputs=[], **kwargs)
            inputs_by_ns = sort_inputs_by_ns(inputs)
            for ns in inputs_by_ns:
                new = fn(self, *args, inputs=inputs_by_ns[ns], **kwargs)
                if isinstance(new, list):
                    old.extend(new)
                elif isinstance(new, dict):
                    old.update(new)
                else:
                    raise NotImplementedError('What datatype?')
            return old
        else:
            return fn(self, *args, inputs=inputs, **kwargs)
    return new_fun

class ReplicatedDatabase(Database):
    """
    define INPUT: pywikibot.Page or id
    """
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

        self._toid = {}
        self._topage = {}
        self._redirect = {}
        self._rv_redirects = defaultdict(list)

    @separate_ns
    def getredirects(self, inputs):
        inputs = self.toid(inputs) # preload
        out = {}
        search = []
        for data in inputs:
            if data in self._redirect:
                out[self.topage(data)] = self._redirect[data]
            else:
                search.append(data)

        if search:
            for result in self.session.query(self.Redirect).filter(self.Redirect.rd_from.in_(search)).all():
                page = pywikibot.Page(self.site,
                                      result.rd_title.decode('utf-8'),
                                      ns=result.rd_namespace)
                self._redirect[result.rd_from] = page
                self._rv_redirects[page].append(result.rd_from)

            for data in search:
                if data in self._redirect:
                    out[self.topage(data)] = self._redirect[data]

        return out

    def toid(self, inputs):
        return self.metaconvert(inputs=inputs, arr=self._toid, typePass=long, typeConvert=pywikibot.Page,
                                filter_kwargs=lambda inputs, ns: [
            self.Page.page_title.in_([page.title(underscore=True, withNamespace=False).encode('utf-8') for page in inputs]),
            self.Page.page_namespace == ns,
        ])

    def topage(self, inputs):
        return self.metaconvert(inputs=inputs, arr=self._topage, typePass=pywikibot.Page, typeConvert=long,
                                filter_kwargs=lambda inputs: [self.Page.page_id.in_(inputs)])

    def toid_final(self, inputs):
        return self.toid(inputs) + self.toid(self.getredirects(inputs=inputs).keys())

    @separate_ns
    def metaconvert(self, inputs, arr, typePass, typeConvert, filter_kwargs):
        if not inputs:
            return []
        if not isinstance(inputs, list):
            single = True
            inputs = [inputs]
        else:
            single = False

        out = []
        search = []
        example = inputs[0]
        if isinstance(example, typeConvert):
            for data in inputs:
                if data in arr:
                    out.append(arr[data])
                else:
                    search.append(data)

            if isinstance(example, pywikibot.Page):
                info = [search, example.namespace()]
            else:
                info = [example]

            if search:
                results = self.session.query(self.Page.page_id, self.Page.page_title).filter(*filter_kwargs(*info)).all()

                for result in results:
                    page = pywikibot.Page(self.site,
                                          result.page_title.decode('utf-8'),
                                          ns=example.namespace())
                    self._topage[result.page_id] = page
                    self._toid[page] = result.page_id

                for data in search:
                    if data in arr:
                        out.append(arr[data])

        elif isinstance(example, typePass):
            out = inputs
        else:
            raise NotImplementedError('Unsupported model')

        if single:
            return out[0]
        else:
            return out

    @separate_ns
    def getlanglinks(self, inputs=[], tolangs=[]):
        """
        Return langlinks of the given input

        @param inputs: list of INPUT, must be called as a kwarg
        @return: a dictionary mapping pywikibot.Page to pywikibot.Page
        """
        langlinks = {}

        args = [self.Langlinks.ll_from.in_(self.toid_final(inputs))] # preload
        if tolangs:
            args.append(self.Langlinks.ll_lang.in_(tolangs))

        results = self.session.query(self.Langlinks).filter(*args).all()
        for result in results:
            page = self.topage(result.ll_from)
            for llpage in self.topage(self._rv_redirects[page]) + [page]:
                langlinks[llpage] = pywikibot.Page(pywikibot.Site(result.ll_lang), result.ll_title.decode('utf-8'))

        return langlinks

if __name__ == "__main__":
    enwp = ReplicatedDatabase()
    enwp.connect(pywikibot.Site())
    print enwp.getlanglinks(inputs=[pywikibot.Page(pywikibot.Site(), 'A'), pywikibot.Page(pywikibot.Site(), 'TeSt Yep')])
    enwp.disconnect()