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

class WikiTranslator(Model):
    def doinit(self, tabactive=None):
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
            error('siteDest', msg['wikitranslator-siteDest-not-found'])
        
        try:
            self.siteSource = pywikibot.Site(self.siteSource)
        except:
            error('siteSource', msg['wikitranslator-siteSource-not-found'])
        
        if self.title:
            self.page = pywikibot.Page(self.siteSource, self.title)
            path = self.exists(self.page)
        
            if path is None:
                error('title', msg['wikitranslator-page-not-found'])

    def dorender(self):
        if self.title:
            self.content = self.page.get()
        
        self.pat = lre.lre(r'~~~#!AmarkerZ@\d+@ZmarkerA!#~~~')
        self.begin = lre.lre(r'~~~#!AahrefZ@\d+@ZahrefA!#~~~')
        self.begintransform = lre.lre(r'~~~#!AahrefZ@(.*?)@ZahrefA!#~~~')
        self.end = lre.lre(r'~~~#!AendaZ@\d+@ZendaA!#~~~')
        self.leadlink = lre.lre(r'^[\[\{]+')
        self.traillink = lre.lre(r'#.*$')
        
        self.cnt = 0
        oldcontent = None
        for tag in ["{{", "[["]:
            while oldcontent != self.content:
                oldcontent = self.content
                self.content = self.content.replace(tag, tag[0] + self.pat.pattern.replace(r'\d+', str(self.cnt)) + tag[1:], 1)
                self.cnt += 1
            oldcontent = None
        self.text = self.content
        self.rmtag('pre')
        self.rmtag('nowiki')
        self.rmtag('source')
        self.content = lre.sub('(?s)<!--.*?-->', '', self.content)
        matches = list(lre.finditer('(?s)(' + self.pat.pattern + r')(.*?)(?=[|}\]])', self.content))
        links = []
        for match in matches:
            links.append(match.group(2))
        translatedLinks = self.translate(links)
        for i, match in enumerate(matches):
            self.text = self.text.replace(match.group(), translatedLinks[i])
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
                #if link.lower().startswith('category:') or ':' not in link:
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
        medium = self.apiquery(links.values())
        for i in links:
            link = pywikibot.Link(links[i], self.siteSource)
            if link in medium:
                links[i] = self.begin.pattern.replace(r'\d+', links[i]) + medium[link] + self.end.pattern
        return links
    
    def apiquery(self, alllinks):
        results = {}
        for links in itergroup(alllinks, 50):
            query = self.siteSource._generator(
                api.PropertyGenerator,
                type_arg="langlinks",
                titles=links,
                redirects='',
                lllang=self.siteDest.code
            )
            firsttime = True
            redirects = DefaultDict()
            normalized = DefaultDict()
            for pageitem in query:
                if firsttime:
                    # a hack to deal with normalization
                    firsttime = False
                    if 'redirects' in query.data['query']:
                        redirects = DefaultDict((item['to'], item['from'])
                                    for item in
                                    query.data['query']['redirects'])
                    normalized = DefaultDict(query.normalized)
                    
                if 'langlinks' not in pageitem:
                    continue
                for linkdata in pageitem['langlinks']:
                    results[pywikibot.Link(normalized[redirects[pageitem['title']]], self.siteSource)] = (
                        linkdata['*']
                    )
        return results
    
    def finalize(self):
        self.text = cgi.escape(self.clean())
        self.text = self.begintransform.sub("<a href='" + '//en.wikipedia.org/wiki/' + r"\1 ' title='\1'>", self.text)
        self.text = self.text.replace(self.end.pattern, '</a>')
    
    def clean(self):
        self.text = self.pat.sub('', self.text).replace('\r', '') # first order
        self.text = lre.sub(r'(?i)\{\{(|' + self.begintransform.pattern + ur')?แม่แบบ:', r'{{\1', self.text)
        self.text = lre.sub(r'(?i)\{\{(|' + self.begintransform.pattern + ur')?Template:', r'{{\1', self.text)
        self.text = lre.sub(r'(?i)\{\{(|' + self.begintransform.pattern + ur')?((?:บทความคัดสรร|บทความคุณภาพ).*?\}\})', 
                            ur'<!-- {{\1\3 หมายเหตุ: นี่คือแม่แบบบทความคัดสรร/คุณภาพที่แปลมาวิกิพีเดียภาษาอื่น โปรดลบทิ้ง -->', self.text)
                            # use \3 because (|' + self.begintransform.pattern + ur') has hidden parentheses.
        self.text = lre.sub(r'(?i)\[\[(|' + self.begintransform.pattern + ur')?Category:', ur'[[\1หมวดหมู่:', self.text)
        self.text = lre.sub(r'(?i)\[\[(|' + self.begintransform.pattern + ur')?(?:Image|File):', ur'[[\1ไฟล์:', self.text)
        self.text = lre.sub(r'(?mi)^== *See also *== *$', u'== ดูเพิ่ม ==', self.text)
        self.text = lre.sub(r'(?mi)^== *External links *== *$', u'== แหล่งข้อมูลอื่น ==', self.text)
        self.text = lre.sub(r'(?mi)^== *References *== *$', u'== อ้างอิง ==', self.text)
        return self.text
    
    def linkvalue(self, link):
        return u"{}:{}".format(self.siteSource.namespace(link.namespace), link.title)