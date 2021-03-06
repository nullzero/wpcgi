#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from utils import AttrObject
from messages import msg
import pywikibot
from wpcgi.model import Template
from utils import TextEngine

class Model(Template):
    def doinit(self):
        self.failed = False
        self.results = []

        self.title = self.form.title.data
        self.oldid = self.form.oldid.data
        self.minlen = int(self.form.minlen.data or 2000)
        self.ratio = float(self.form.ratio.data or 2.0)
        self.maxday = int(self.form.maxday.data or 14)

    def dovalidate(self):
        self.site = pywikibot.Site('th')
        self.page = pywikibot.Page(self.site, self.title)

        path = self.exists(self.page)
        if path is None:
            self.error('title', msg['dykchecker-page-not-found'])
        elif path:
            self.page = path[-1]

        if self.oldid:
            try:
                self.oldid = self.site.loadrevid(self.oldid)
            except:
                self.error('oldid', msg['dykchecker-oldid-not-found'])

    def dorender(self):
        self.textEngine = TextEngine()
        self.text = self.page.get()

        self.check_info()
        self.check_ref()
        self.check_length()
        self.check_old()

        result = AttrObject(cl=self.evaluate(not self.failed),
                            text=msg['dykchecker-summary'],
                            desc='')

        if self.failed:
            result.value = msg['dykchecker-summary-fail']
        else:
            result.value = msg['dykchecker-summary-pass']

        self.results.insert(0, result)

        self.results = enumerate(self.results)

    def evaluate(self, val):
        if val:
            return "passed"
        else:
            self.failed = True
            return "failed"

    def neutral(self):
        return "normal"

    def check_info(self):
        self.results.append(
            AttrObject(cl=self.neutral(),
                       value=msg['dykchecker-revision-info-value'].format(
                           self.page.latestRevision(),
                           self.page.title(),
                           self.page.userName(),
                           self.page.editTime()
                       ),
                       text=msg["dykchecker-revision-info"],
                       desc="",
            )
        )

    def check_ref(self):
        allrefs = self.text.count("<ref")
        self.results.append(
            AttrObject(cl=self.evaluate(allrefs > 0),
                       value=msg['dykchecker-inlineref-value'].format(allrefs),
                       text=msg["dykchecker-inlineref"],
                       desc=msg["dykchecker-inlineref-desc"]
            )
        )

    def check_length(self):
        self.text = self.textEngine.remove(self.text)
        self.length, self.swath = self.textEngine.length(self.text)
        self.results.append(
            AttrObject(cl=self.evaluate(self.length > self.minlen),
                       value=msg['dykchecker-length-value'].format(self.length),
                       text=msg["dykchecker-length"],
                       desc=msg["dykchecker-length-desc"].format(self.minlen),
            )
        )
        self.text = self.textEngine.convert(self.text)

    def check_old(self):
        now = self.site.getcurrenttime()
        oldestRev = None
        newArt = False
        if self.oldid:
            oldestRev = self.oldid
        else:
            for revision in self.page.getVersionHistory():
                if (now - revision[1]).days > self.maxday:
                    break
                oldestRev = revision
            else:
                createRev = oldestRev
                newArt = True

            if not newArt:
                createRev = self.page.getVersionHistory(reverseOrder=True, total=1)[0]

            if newArt:
                article_creation_desc = msg["dykchecker-creation-new-desc"].format(self.maxday)
                article_creation_eval = self.evaluate(True)
            else:
                article_creation_desc = msg["dykchecker-creation-desc"]
                article_creation_eval = self.neutral()

            self.results.append(
                AttrObject(text=msg["dykchecker-creation"],
                           desc=msg[article_creation_desc],
                           cl=article_creation_eval,
                           value=msg['dykchecker-creation-value'].format(
                               createRev[0], createRev[1], createRev[2], (now - createRev[1]).days
                           )
                )
            )

            if newArt:
                return

        result = AttrObject(text=msg["dykchecker-old-revision"],
                            desc=msg["dykchecker-old-revision-desc"].format(self.ratio, self.maxday))

        if oldestRev is None:
            result.cl = self.evaluate(False)
            result.value = msg['dykchecker-old-revision-not-exist'].format(self.maxday)
        else:
            if self.oldid:
                text = oldestRev[3]
            else:
                text = self.page.getOldVersion(oldestRev[0], get_redirect=True)
            text = self.textEngine.remove(text)
            length = self.textEngine.length(text)[0]
            ratio = float(self.length) / float(length)
            result.cl = self.evaluate(ratio >= (self.ratio + 1))
            result.value = msg['dykchecker-old-revision-value'].format(
                oldestRev[0], oldestRev[1], (now - oldestRev[1]).days, length, ratio - 1.0
            )
        self.results.append(result)