#!/data/project/nullzerobot/python/bin/python

from wtforms.validators import *
from wtforms.validators import ValidationError
from messages import msg
import re

##############################

class _Required(Required):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('message', False):
            kwargs['message'] = msg['validator-require']
        super(_Required, self).__init__(*args, **kwargs)

Required = _Required

##############################

class _NumberRange(NumberRange):
    def __init__(self, *args, **kwargs):
        if 'message' not in kwargs:
            kwargs['message'] = msg['validator-mustbe-in-min-max']
        super(_NumberRange, self).__init__(*args, **kwargs)

NumberRange = _NumberRange

##############################

class _Email(Email):
    def __init__(self, *args, **kwargs):
        if 'message' not in kwargs:
            kwargs['message'] = msg['validator-invalid-email']
        super(_Email, self).__init__(*args, **kwargs)

Email = _Email

##############################

def Number(negative=False, decimal=False):
    charset = r'\d'
    if negative:
        charset += '-'
    if decimal:
        charset += r'\.'

    def _Number(form, field):
        if not field.data or not re.match('^[' + charset + ']+$', field.data):
            raise ValidationError(msg['validator-not-number'])

    return _Number

##############################

class IgnoreMe(object):
    def __init__(self, *args, **kwargs):
        pass

    __call__ = __init__

##############################