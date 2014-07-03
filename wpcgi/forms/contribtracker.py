#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField, TextAreaField, HiddenField, SubmitField
from messages import msg

class ContribTrackerForm(Form):
    pass

def ContribTrackerFormCreator():
    FormCl = ContribTrackerForm
    FormCl.title = TextField(msg['contribtracker-title-label'],
                                 id='txt-title')
    FormCl.content = TextAreaField(msg['contribtracker-content-label'],
                                   id="txt-content")
    FormCl.tabStatus = HiddenField(id="tab-active", validators=[v.IgnoreMe()])
    FormCl.proceed = SubmitField(msg['contribtracker-button-submit'])
    return FormCl