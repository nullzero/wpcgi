#!/data/project/nullzerobot/python/bin/python

from p_form import Form, c_validators
from wtforms import TextField
from wtforms.widgets import SubmitInput
from messages import msg
from models import DYKChecker

class DYKCheckerForm(Form):
    title = TextField(msg['dykchecker-label-title'],
                      id='txt-title',
                      validators=[c_validators.Required()])
    oldid = TextField(msg['dykchecker-label-oldid'],
                      id='txt-oldid',
                      validators=[c_validators.Number(), c_validators.Optional()])
    minlen = TextField(msg['dykchecker-label-minlen'],
                       validators=[c_validators.Number(), c_validators.Optional()])
    ratio = TextField(msg['dykchecker-label-ratio'],
                      validators=[c_validators.Number(decimal=True),
                                  c_validators.NumberRange(min=1.0),
                                  c_validators.Optional()])
    maxday = TextField(msg['dykchecker-label-maxday'],
                       validators=[c_validators.Number(),
                                   c_validators.Optional(),
                                   c_validators.NumberRange(min=1, max=30)])