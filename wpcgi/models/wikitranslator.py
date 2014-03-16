#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import cgi
from messages import msg
import pyrobot
import pywikibot
from pywikibot.data import api
from pywikibot.tools import itergroup
from wp import lre
import wp
from model import Model
from utils import DefaultDict
from p_flask import g, current_app

class WikiTranslator(Model):
    def doinit(self, tabactive):
        self.tabactive = tabactive or 'page'
        self.isActivePage = 'active'
        self.isActiveContent = ''
        if tabactive == 'content':
            self.isActivePage, self.isActiveContent = self.isActiveContent, self.isActivePage

        self.text = None
        self.title = self.form.title.data
        self.siteDest = self.form.siteDest.data
        self.siteSource = self.form.siteSource.data
        self.content = self.form.content.data

    def dovalidate(self):
        try:
            self.siteDest = pywikibot.Site(self.siteDest)
        except:
            self.error('siteDest', msg['wikitranslator-siteDest-not-found'])

        try:
            self.siteSource = pywikibot.Site(self.siteSource)
        except:
            self.error('siteSource', msg['wikitranslator-siteSource-not-found'])

        if self.tabactive == 'page':
            if self.title:
                self.page = pywikibot.Page(self.siteSource, self.title)
                path = self.exists(self.page)

                if path is None:
                    self.error('title', msg['wikitranslator-page-not-found'])
                elif path:
                    self.page = path[-1]
            else:
                self.error('title', msg['validator-require'])
        else:
            if not self.content:
                self.error('content', msg['validator-require'])

    def dorender(self):
        if self.tabactive == 'page':
            self.content = self.page.get()

        self.pat_before = '~~~#m!'
        self.pat_after = self.pat_before[::-1]
        self.pat = self.pat_before + r'\d+' + self.pat_after

        self.begin_assert = '((?:(?!~~~).)*?)'
        self.begin = '~~~#h!'
        self.begin = self.begin + self.begin_assert + self.begin[::-1]

        self.end = '~~~#e!'

        self.leadlink = lre.lre(r'^[\[\{]+')
        self.traillink = lre.lre(r'#.*$')

        self.cnt = 0
        self.text = []
        ptr = 0
        while ptr < len(self.content):
            if self.content[ptr:ptr+2] == '{{' or self.content[ptr:ptr+2] == '[[':
                self.text.append(self.content[ptr])
                self.text.append(self.pat_before)
                self.text.append(str(self.cnt))
                self.cnt += 1
                self.text.append(self.pat_after)
                self.text.append(self.content[ptr + 1])
                ptr += 2
            else:
                self.text.append(self.content[ptr])
                ptr += 1

        self.text = ''.join(self.text)
        self.content = self.text
        self.rmtag('pre')
        self.rmtag('nowiki')
        self.rmtag('source')
        self.content = lre.sub('(?s)<!--.*?-->', '', self.content)
        matches = list(lre.finditer('(?s)(' + self.pat + r')(.*?)(?=[|}\]\n])', self.content))
        links = []
        for match in matches:
            links.append(match.group(2))
        translatedLinks = self.translate(links)
        for i, match in enumerate(matches):
            self.text = self.text.replace(match.group(), translatedLinks[i], 1)
        self.finalize()

    def rmtag(self, tag):
        self.content = lre.sub("(?s)<{tag}>.*?</{tag}>".format(tag=tag), "", self.content)

    def translate(self, links):
        """
        Translate links
        """
        totranslate = {}
        processed = []
        for i, link in enumerate(links):
            if link.startswith('['):
                link = self.leadlink.sub('', link)
                link = self.traillink.sub('', link)
                totranslate[i] = link
            elif link.startswith('{'):
                link = self.leadlink.sub('', link)
                if ':' not in link:
                    totranslate[i] = 'Template:' + link
                else:
                    totranslate[i] = link
            else:
                raise Exception('wait what?')
            processed.append(link)

        translated = self._translate(totranslate)
        for i, link in enumerate(links):
            if i in translated:
                links[i] = link.replace(processed[i], translated[i])
        return links

    def _translate(self, links):
        """
        Translate links by inserting <a> tag
        """
        if current_app.config['SQL']:
            from replicateddb import Database
            pages = {pywikibot.Page(self.siteSource, links[i]): links[i] for i in links}
            db = Database()
            try:
                db.connect(site=self.siteSource)
                results = db.langlinks(frompages=pages, tolangs=[self.siteDest.code])
                medium = {}
                for page_lang in results:
                    medium[pages[page_lang[0]]] = results[page_lang]
                db.disconnect()
            except:
                db.disconnect()
                raise
        else:
            medium = self.apiquery(links.values())

        for i in links:
            if links[i] in medium:
                old = links[i]
                new = medium[links[i]]
                if (pywikibot.Page(self.siteDest, old).title().lower() ==
                    pywikibot.Page(self.siteDest, new).title().lower()):
                    if old.lower() == old:
                        new = new.lower()
                    elif old.upper() == old:
                        new = new.upper()
                links[i] = self.begin.replace(self.begin_assert, old) + new + self.end
        return links

    def apiquery(self, alllinks):
        output = {}
        for links in itergroup(alllinks, 50):
            query = api.Request(site=self.siteSource, action='query', prop='langlinks', titles=links,
                                redirects='', lllang=self.siteDest.code, lllimit=500)
            results = query.submit()
            if 'query-continue' in results:
                raise Exception('should not get query-continue')
            if 'query' not in results:
                continue
            results = results['query']
            redirects = DefaultDict()
            normalized = DefaultDict()
            if 'pages' not in results:
                continue
            if 'redirects' in results:
                redirects = DefaultDict((item['to'], item['from'])
                                        for item in results['redirects'])
            if 'normalized' in results:
                normalized = DefaultDict((item['to'], item['from'])
                                         for item in results['normalized'])
            results = results['pages']
            for pageid in results:
                if int(pageid) < 0:
                    continue
                pagedata = results[pageid]
                if 'langlinks' not in pagedata:
                    continue
                output[normalized[redirects[pagedata['title']]]] = pagedata['langlinks'][0]['*']
        return output

    def finalize(self):
        self.text = cgi.escape(self.clean())
        self.text = lre.sub(r'(?is)' + self.begin, "<a href='" + '//' + self.siteSource.code + '.wikipedia.org/wiki/' + r"\1 ' title='\1'>", self.text)
        self.text = self.text.replace(self.end, '</a>')

    def clean(self):
        self.text = lre.sub(self.pat, '', self.text).replace('\r', '') # first order
        self.text = lre.sub(r'(?is)\{\{(|' + self.begin + ur')?(?:{}):'.format('|'.join(self.siteDest.namespaces()[10])), r'{{\1', self.text)
        pat = r'(?is)\{\{(|' + self.begin + ')?((?:' + msg['wikitranslator-fa/ga-tag'] + r').*?\}\})'
        self.text = lre.sub(pat, r'<!-- {{\1\3 ' + msg['wikitranslator-fa/ga-notice'] + ' -->', self.text)
                            # use \3 because self.begin has a hidden parenthesis.
        self.text = lre.sub(r'(?is)\[\[(|' + self.begin + ur')?Category:', ur'[[\1หมวดหมู่:', self.text)
        self.text = lre.sub(r'(?is)\[\[(|' + self.begin + ur')?(?:Image|File):', ur'[[\1ไฟล์:', self.text)
        self.text = lre.sub(r'(?mi)^== *See also *== *$', u'== ดูเพิ่ม ==', self.text)
        self.text = lre.sub(r'(?mi)^== *External links *== *$', u'== แหล่งข้อมูลอื่น ==', self.text)
        self.text = lre.sub(r'(?mi)^== *References *== *$', u'== อ้างอิง ==', self.text)
        return self.text

"""
Ineffective code?: translate links

len(self.text) <= 1000000
len(matches) <= 1000


ptr = 0
self.content = []
while ptr < len(self.text):
    for i in matches:
        match = matches[i]
        strlen = len(match.group())
        text = self.text[ptr:ptr+strlen]
        if text == match.group():
            ptr += strlen
            self.content.append(translatedLinks[i])
            del matches[i]
            break
    else:
        self.content.append(self.text[ptr])
        ptr += 1
self.text = ''.join(self.content)
"""
