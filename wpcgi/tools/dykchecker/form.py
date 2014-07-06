#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField, SubmitField
from messages import msg

class DYKCheckerForm(Form):
    pass

def getForm():
    FormCl = DYKCheckerForm
    FormCl.title = TextField(msg['dykchecker-title-label'],
                                 id='txt-title',
                                 validators=[v.Required()])
    FormCl.oldid = TextField(msg['dykchecker-oldid-label'],
                             id='txt-oldid',
                             validators=[v.Number(),
                                         v.Optional()])
    FormCl.minlen = TextField(msg['dykchecker-minlen-label'],
                              validators=[v.Number(),
                                          v.Optional()])
    FormCl.ratio = TextField(msg['dykchecker-ratio-label'],
                             validators=[v.Number(decimal=True),
                                         v.NumberRange(min=1.0),
                                         v.Optional()])
    FormCl.maxday = TextField(msg['dykchecker-maxday-label'],
                              validators=[v.Number(),
                                          v.Optional(),
                                          v.NumberRange(min=1, max=30)])
    FormCl.proceed = SubmitField(msg['dykchecker-button-submit'])
    return FormCl