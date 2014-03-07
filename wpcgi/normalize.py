from functools import wraps
from p_flask import redirect, url_for
import c

def normalize_url_title(dic):
    title = dic.get('title', None)
    if not title:
        return False
    new_title = (title.replace(' ', '_'))
    if new_title != title:
        dic['title'] = new_title
        return True
    return False

def normalize_title(dic):
    title = dic.get('title', None)
    if not title:
        return False
    new_title = (title.replace('_', ' '))
    if new_title != title:
        dic['title'] = new_title
        return True
    return False

def normalize_url(L):
    def outter(fn):
        @wraps(fn)
        def new_fn(*args, **kwargs):
            change = False
            for key in L:
                if key == 'title':
                    change = change or normalize_url_title(kwargs)
            if change:
                return redirect(url_for('.' + fn.__name__, **kwargs), code=c.REQUEST)
            else:
                return fn(**kwargs)
        return new_fn
    return outter

def normalize(L, dic):
    for key in L:
        if key == 'title':
            normalize_title(dic)