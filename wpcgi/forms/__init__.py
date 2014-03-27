#!/data/project/nullzerobot/python/bin/python

from wtforms import SelectField
from messages import msg

def lang_default(*args, **kwargs):
    return SelectField(*args, choices=[
        ('th', msg['form-lang-th']),
        ('en', msg['form-lang-en']),
        ('de', msg['form-lang-de']),
        ('fr', msg['form-lang-fr']),
        ('it', msg['form-lang-it']),
        ('ru', msg['form-lang-ru']),
        ('vi', msg['form-lang-vi']),
        ('zh', msg['form-lang-zh']),
    ], **kwargs)

def fam_default(*args, **kwargs):
    return SelectField(*args, choices=[
        ('wikipedia', msg['form-fam-wikipedia']),
        ('wikibooks', msg['form-fam-wikibooks'])
    ], **kwargs)