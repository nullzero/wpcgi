#!/data/project/nullzerobot/python/bin/python

import wtforms.validators
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

wtforms.validators.Required = _Required

##############################

class _NumberRange(NumberRange):
    def __init__(self, *args, **kwargs):
        if 'message' not in kwargs:
            kwargs['message'] = msg['validator-mustbe-in-min-max']
        super(_NumberRange, self).__init__(*args, **kwargs)

wtforms.validators.NumberRange = _NumberRange

##############################

# Have to do like this because the original Email.__init__ contains Email itself
def Email__init__(self, message=msg['validator-invalid-email']):
    super(Email, self).__init__(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE, message)

wtforms.validators.Email.__init__ = Email__init__

##############################

def _Number(negative=False, decimal=False):
    charset = r'\d'
    if negative:
        charset += '-'
    if decimal:
        charset += r'\.'

    def _Number(form, field):
        if not field.data or not re.match('^[' + charset + ']+$', field.data):
            raise ValidationError(msg['validator-not-number'])

    return _Number

wtforms.validators.Number = _Number

##############################

class _IgnoreMe(object):
    def __init__(self, *args, **kwargs):
        pass

    __call__ = __init__

wtforms.validators.IgnoreMe = _IgnoreMe

##############################
