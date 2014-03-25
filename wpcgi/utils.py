#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from p_flask import request, g, flash

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
            flash(e.flash_msg, e.flash_level)
    else:
        hasError = False
    if hasError:
        return local['onFail']()
    else:
        return local['onSuccess'](result)
