#!/data/project/nullzerobot/python/bin/python

import flask.ext.wtf
from flask.ext.wtf import *
from flask import request
from messages import msg
from werkzeug.datastructures import MultiDict
import wtforms.validators as v

class _Form(Form):
    def __init__(self, *args, **kwargs):
        args = list(args)
        if args:
            self.request = args[0]
            args[0] = MultiDict(args[0])
            args[0].update(kwargs)
        super(_Form, self).__init__(*args, csrf_enabled=False)
        for field in self.data:
            field = getattr(self, field)
            for validator in field.validators:
                if isinstance(validator, v.Required):
                    field.label.text = (u'{0}<span class="required">{1}</span>').format(
                        field.label.text, msg['core-required-symbol'])

    def validate(self, data=None):
        def isInteracting():
            if request.form:
                return True
            for fieldname in self.data:
                field = getattr(self, fieldname)
                ignore = False
                for validator in field.validators:
                    if isinstance(validator, v.IgnoreMe):
                        ignore = True
                        break
                if not ignore and self.data[fieldname]:
                    return True
            return False

        interacting = isInteracting()

        fail = False

        if not super(_Form, self).validate():
            fail = True
        if not fail and data:
            errors = data.validate()
            for field in errors:
                getattr(self, field).errors.extend(errors[field])
            if errors:
                fail = True

        if fail:
            if not interacting:
                for fieldname in self.data:
                    field = getattr(self, fieldname)
                    field.errors = []
            return False
        return True

flask.ext.wtf.Form = _Form
