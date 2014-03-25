#!/data/project/nullzerobot/python/bin/python

from wtforms import SelectField
from messages import msg


def lang_default(*args, **kwargs):
    return SelectField(*args, choices=[
        ('th', msg['form-lang-th']),
        ('en', msg['form-lang-en'])
    ], **kwargs)

def fam_default(*args, **kwargs):
    return SelectField(*args, choices=[
        ('wikipedia', msg['form-fam-wikipedia']),
        ('wikibooks', msg['form-fam-wikibooks'])
    ], **kwargs)