#!/data/project/nullzerobot/python/bin/python

from p_form import Form, c_validators as v
from wtforms import TextField
from wtforms.widgets import SubmitInput
from messages import msg
from models import DYKChecker

class DYKCheckerForm(Form):
    pass

def DYKCheckerFormCreator():
    FormCl = DYKCheckerForm
    FormCl.title = TextField(msg['dykchecker-label-title'],
                                 id='txt-title',
                                 validators=[v.Required()])
    FormCl.oldid = TextField(msg['dykchecker-label-oldid'],
                             id='txt-oldid',
                             validators=[v.Number(),
                                         v.Optional()])
    FormCl.minlen = TextField(msg['dykchecker-label-minlen'],
                              validators=[v.Number(),
                                          v.Optional()])
    FormCl.ratio = TextField(msg['dykchecker-label-ratio'],
                             validators=[v.Number(decimal=True),
                                         v.NumberRange(min=1.0),
                                         v.Optional()])
    FormCl.maxday = TextField(msg['dykchecker-label-maxday'],
                              validators=[v.Number(),
                                          v.Optional(),
                                          v.NumberRange(min=1, max=30)])
    return DYKCheckerForm