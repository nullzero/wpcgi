#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form

def getField(template, fieldlist=True):
    class Dummy(Form):
        pass

    if fieldlist is True:
        return template

    for field in fieldlist:
        setattr(Dummy, field, getattr(template, field))

    return Dummy
