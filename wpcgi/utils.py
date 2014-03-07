#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-
"""
    Utils has nothing to do with models and views.
"""

from datetime import datetime
from p_flask import request


VARCHAR_LEN_128 = 128


def get_current_time():
    return datetime.utcnow()


def pretty_date(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
    """

    if default is None:
        default = 'just now'

    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days / 30, 'month', 'months'),
        (diff.days / 7, 'week', 'weeks'),
        (diff.days, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds / 60, 'minute', 'minutes'),
        (diff.seconds, 'second', 'seconds'),
    )

    for period, singular, plural in periods:

        if not period:
            continue

        if period == 1:
            return u'%d %s ago' % (period, singular)
        else:
            return u'%d %s ago' % (period, plural)

    return default

class AttrObject(dict):
    def __init__(self, *args, **kwargs):
        super(AttrObject, self).__init__(*args, **kwargs)
        self.__dict__ = self

def get_params(L):
    dic = {}
    for name in L:
        var = request.form.get(name, None)
        if var:
            dic[name] = var
    return dic