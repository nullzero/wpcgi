#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import pyrobot
import pywikibot
from wp import lre
from p_flask import request, g, flash, url_for
import subprocess
import cgi

class AttrObject(dict):
    def __init__(self, *args, **kwargs):
        super(AttrObject, self).__init__(*args, **kwargs)
        self.__dict__ = self

class DefaultDict(dict):
    def __missing__(self, key):
        return key

def get_params(L):
    dic = {}
    for name in L:
        var = request.form.get(name, None)
        if var:
            dic[name] = var
    return dic

import cProfile as profiler
import gc, pstats, time


def profile(fn):
    def wrapper(*args, **kw):
        elapsed, stat_loader, result = _profile("foo.txt", fn, *args, **kw)
        stats = stat_loader()
        stats.sort_stats('cumulative')
        stats.print_stats()
        # uncomment this to see who's calling what
        # stats.print_callers()
        return result
    return wrapper

def _profile(filename, fn, *args, **kw):
    load_stats = lambda: pstats.Stats(filename)
    gc.collect()

    began = time.time()
    profiler.runctx('result = fn(*args, **kw)', globals(), locals(),
                    filename=filename)
    ended = time.time()

    return ended - began, load_stats, locals()['result']

def debug(*args, **kwargs):
    g.debugtext += g.request_time() + ': ['
    with_repr = kwargs.get('with_repr', True)
    for arg in args:
        if with_repr:
            g.debugtext += repr(arg) + ', '
        else:
            g.debugtext += arg + ', '
    g.debugtext += ']<br/>\n'

def newtry(local):
    hasError = True
    try:
        result = local['fun']()
    except Exception, e:
        if hasattr(e, 'flash_msg'):
            if e.flash_msg:
                flash(e.flash_msg, e.flash_level)
        else:
            raise e
    else:
        hasError = False
    if hasError:
        return local['onFail']()
    else:
        return local['onSuccess'](result)

def gourl(default='frontend.index'):
    return (request.args.get('next') or
            request.referrer or
            url_for(default))

class TextEngine(object):
    def __init__(self):
        self.subst = lre.Subst()
        self.op = "~~~#o!"
        self.ed = "~~~#c!"

        self.subst.append(r"[ \t]+", " ")

        self.removePair("<!--", "-->")
        self.removePair("{|", "|}")
        self.removePair("{{", "}}")

        self.removeTag("gallery")
        self.removeTag("div")
        self.removeTag("math")
        self.removeTag("table")
        self.removeTag("score")
        self.removeTag("source")
        self.removeTag("pre")
        self.removeTag("syntaxhighlight")
        self.removeTag("poem")
        self.removeTag("ref")


        self.subst.append(
            r"(\[\[[^\]\|\[]*\|)(.*?)(\]\])", r"{}\1{}\2{}\3{}".format(
                self.op, self.ed, self.op, self.ed
            )
        )

        self.removePart(r"(< ?/? ?(br|center|sup|sub|nowiki|ref) ?/? ?>)")
        #self.removePart(r"(<ref[^>]*?/ ?>)")
        #self.removePart(r"(?s)(<ref[^>/]*?>.*?</ref>)")
        self.removePart(r"(?s)(?<!\[)(\[(?!\[) *http://.*?\])")
        self.removePart(r"(https?://\S*)")
        self.removePart(r"(?s)(\[\[[^\]\|]*?\:.*?\]\])")
        self.removePart(r"(\'{2,})")
        self.removePart(ur"(?ms)^(== ?(อ้างอิง|ดูเพิ่ม|แหล่งข้อมูลอื่น|เชิงอรรถ) ?== ?$.*)$")
        self.removePart(r"(?m)(^=+ ?|=+ ?$)")
        self.removePart(r"(?m)^([\:\*\#\;]+)")

        self.removePair("[", "[")
        self.removePair("]", "]")
        self.removePair("(", "(")
        self.removePair(")", ")")
        self.removePair('"', '"')
        self.removePair(',', ',')

        self.subst.append(self.ed + self.op, '')

    def removeTag(self, tag):
        self.removePair('<{}'.format(tag), '</{}>'.format(tag))

    def removePair(self, begin, end):
        self.subst.append(lre.escape(begin), self.op + begin)
        self.subst.append(lre.escape(end), end + self.ed)

    def removePart(self, pat):
        self.subst.append(pat, self.op + r"\1" + self.ed)

    def remove(self, text):
        return self.subst.process(text)

    def convert(self, text):
        return (cgi.escape(text).replace("\n", "<br/>")
                                .replace(self.op, '<span class="eqtext">')
                                .replace(self.ed, '</span>'))

    def length(self, text):
        delim = "THISISASECRETKEYYOUWILLNEVERKNOW"
        text = (text.replace(self.op, "(")
                    .replace(self.ed, ")"))
        level = 0
        charlimit = 0
        trimtext = []
        for i in text:
            if i == "(" or i == ")" or level == 0:
                if i == "(":
                    level += 1
                elif i == ")":
                    level -= 1
                else:
                    charlimit += 1
                trimtext.append(i)

        trimtext = "".join(trimtext)

        p = subprocess.Popen(["/data/project/nullzerobot/local/bin/swath", "-b", delim, "-u", "u,u"],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        output = p.communicate(input=trimtext.encode('utf-8'))[0].decode('utf-8')
        text = []
        blacklist = [" ", "\n", "(", ")"]
        for i in output:
            if i in blacklist:
                text.append(delim)
                text.append(i)
                text.append(delim)
            else:
                text.append(i)
        text = "".join(text)
        text = text.replace(delim + delim, delim)
        cnt = 0
        allwords = (list(lre.finditer('^(?!{delim}).*?(?={delim})'.format(delim=delim), text)) +
                    list(lre.finditer('(?<={delim}).*?(?={delim})'.format(delim=delim), text)) +
                    list(lre.finditer('(?<={delim}).*?(?!{delim})$'.format(delim=delim), text)))
        output = []
        for item in allwords:
            if item.group() not in blacklist:
                cnt += 1
                output.append(item.group().replace('[', '(').replace(']', ')'))
        print cnt, charlimit / 2, charlimit / 12
        cnt = max(cnt, charlimit / 10)
        cnt = min(cnt, charlimit / 2)
        return (cnt, " ".join(output))
