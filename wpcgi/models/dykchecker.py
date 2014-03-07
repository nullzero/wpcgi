# -*- coding: utf-8 -*-

import cgi
from utils import AttrObject
from messages import msg
import pyrobot
import pywikibot
from wp import lre

class RemoveEngine(object):
    def __init__(self):
        self.subst = lre.Subst()
        self.op = "~~~OPENSESAME~~~"
        self.ed = "~~~CLOSESESAME~~~"
        
        self.subst.append(r"[ \t]+", " ")
        
        self.removePair("<!--", "-->")
        self.removePair("{|", "|}")
        self.removePair("{{", "}}")
        self.removePair("<gallery>", "</gallery>")
        self.removePair("<div", "</div>")
        self.removePair("<math>", "</math>")
        
        self.subst.append(
            r"(\[\[[^\]\|\[]*\|)(.*?)(\]\])", r"{}\1{}\2{}\3{}".format(
                self.op, self.ed, self.op, self.ed
            )
        )
        
        self.removePart(r"(< ?/? ?(br|center|sup|sub) ?/? ?>)")
        self.removePart(r"(<br ?/? ?>)")
        self.removePart(r"(<ref[^>]*?/ ?>)")
        self.removePart(r"(?s)(<ref[^>/]*?>.*?</ref>)")
        self.removePart(r"(?s)(?<!\[)(\[(?!\[) *http://.*?\])")
        self.removePart(r"(https?://\S*)")
        self.removePart(r"(?s)(\[\[[^\]\|]*?\:.*?\]\])")
        self.removePart(r"(\'{2,})")
        self.removePart(ur"(?ms)^(== ?(อ้างอิง|ดูเพิ่ม|แหล่งข้อมูลอื่น|เชิงอรรถ) ?== ?$.*)$")
        self.removePart(r"(?m)(^=+ ?|=+ ?$)")
        self.removePart(r"(?m)^([\:\*\#]+)")
        
        self.removePair("[", "[")
        self.removePair("]", "]")
        
    def removePair(self, begin, end):
        self.subst.append(lre.escape(begin), self.op + begin)
        self.subst.append(lre.escape(end), end + self.ed)
    
    def removePart(self, pat):
        self.subst.append(pat, self.op + r"\1" + self.ed)
        
    
    def process(self, text):
        return self.subst.process(text)
    
    def convert(self, text):
        return (cgi.escape(text).replace("\n", "<br/>")
                                .replace(self.op, '<span class="eqtext">')
                                .replace(self.ed, '</span>'))
    
    def length(self, text):
        text = (text.replace("(", "[")
                    .replace(")", "]")
                    .replace(self.op, "(")
                    .replace(self.ed, ")"))
        level = 0
        ans = 0
        for i in text:
            if i == "(":
                level += 1
            elif i == ")":
                level -= 1
            elif level == 0 and self.valid(i):
                ans += 1
        return ans
    
    def valid(self, ch):
        blacklist = [" ", "\n"]
        return ch not in blacklist
        

class DYKChecker(object):
    def __init__(self, form):
        self.is_validate = False
        
        self.errors = {}
        
        self.failed = False
        self.results = []
        
        self.path = []
        
        self.form = form
        self.title = form.title.data
        self.oldid = form.oldid.data
        
    def validate(self):
        self.is_validate = True
        
        self.site = pywikibot.Site("th")
        self.page = pywikibot.Page(self.site, self.title)
    
        while self.page.exists():
            if self.page.isRedirectPage():
                self.page = self.page.getRedirectTarget()
                self.path.append(self.page.title())
            else:
                break
        else:
            self.error('title', msg['dykchecker-page-not-found'])
    
        return self.errors
    
    def render(self):
        if not self.is_validate:
            raise Exception('Must validate first')
            
        self.removeEngine = RemoveEngine()
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
        
    def error(self, field, m):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(m)
    
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
        self.text = self.removeEngine.process(self.text)
        self.length = self.removeEngine.length(self.text)
        self.results.append(
            AttrObject(cl=self.evaluate(self.length > 2000),
                       value=msg['dykchecker-length-value'].format(self.length),
                       text=msg["dykchecker-length"],
                       desc=msg["dykchecker-length-desc"],
            )
        )
        self.text = self.removeEngine.convert(self.text)
    
    def check_old(self):
        now = self.site.getcurrenttime()
        oldestRev = None
        newArt = False
        for revision in self.page.getVersionHistory():
            if (now - revision[1]).days > 14:
                break
            oldestRev = revision
        else:
            createRev = oldestRev
            newArt = True
        
        if not newArt:
            createRev = self.page.getVersionHistory(reverseOrder=True, total=1)[0]
        
        if newArt:
            article_creation_desc = msg["dykchecker-creation-new-desc"]
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
        
        if newArt: return
        
        result = AttrObject(text=msg["dykchecker-old-revision"],
                            desc=msg["dykchecker-old-revision-desc"])
        
        if oldestRev is None:
            result.cl = self.evaluate(False)
            result.value = msg['dykchecker-old-revision-not-exist']
        else:
            text = self.page.getOldVersion(oldestRev[0], get_redirect=True)
            text = self.removeEngine.process(text)
            length = self.removeEngine.length(text)
            ratio = float(self.length) / float(length)
            result.cl = self.evaluate(ratio > 3.0)
            result.value = msg['dykchecker-old-revision-value'].format(
                oldestRev[0], oldestRev[1], (now - oldestRev[1]).days, length, ratio - 1.0
            )
        self.results.append(result)