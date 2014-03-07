#!/data/project/nullzero/python/bin/python

from flask.ext.wtf import *
from p_flask import request

class _Form(Form):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(_Form, self).__init__(*args, **kwargs)
    
    def validate(self, data=None):
        if not request.form and not any(self.data.values()):
            return False
        if not super(_Form, self).validate():
            return False
        if data:
            errors = data.validate()
            for field in errors:
                getattr(self, field).errors.extend(errors[field])
            if errors:
                return False
        return True

Form = _Form
