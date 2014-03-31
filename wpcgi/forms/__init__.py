#!/data/project/nullzerobot/python/bin/python

from wtforms import SelectField
from messages import msg

def fam_default(*args, **kwargs):
    return SelectField(*args, choices=[
        ('wikipedia', msg['form-fam-wikipedia']),
        ('wikibooks', msg['form-fam-wikibooks'])
    ], **kwargs)