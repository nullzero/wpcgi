#!/data/project/nullzerobot/python/bin/python

from forms.dykchecker import DYKCheckerFormCreator
from forms.categorymover import CategoryMoverFormCreator
from wtforms import SelectField
from messages import msg

fam_default_list = [
    ('wikipedia', msg['form-fam-wikipedia']),
    ('wikibooks', msg['form-fam-wikibooks'])
]

lang_default_list = [
    ('th', msg['form-lang-th']),
    ('en', msg['form-lang-en'])
]

fam_default = SelectField(msg['form-fam'], choices=fam_default_list)

def lang_default(*args, **kwargs):
    return SelectField(*args, choices=lang_default_list, **kwargs)

def fam_default(*args, **kwargs):
    return SelectField(*args, choices=fam_default_list, **kwargs)