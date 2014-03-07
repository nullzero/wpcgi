#!/data/project/nullzerobot/python/bin/python

from wtforms.validators import *
from wtforms.validators import ValidationError
from messages import msg
import re

class _Required(Required):
    def __init__(self, *args, **kwargs):
        if kwargs.get('message', False):
            kwargs['message'] = msg['validator-require']
        super(_Required, self).__init__(*args, **kwargs)

Required = _Required

def Number(negative=False, decimal=False):
    charset = r'\d'
    if negative:
        charset += '-'
    if decimal:
        charset += r'\.'
        
    def _Number(form, field):
        if not field.data or not re.match('[' + charset + ']+', field.data):
            raise ValidationError(msg['validator-not-integer'])
            
    return _Number