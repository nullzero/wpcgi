#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form

def getField(template, fieldlist):
    class Dummy(Form):
        pass

    for field in fieldlist:
        setattr(Dummy, field, getattr(template, field))

    return Dummy