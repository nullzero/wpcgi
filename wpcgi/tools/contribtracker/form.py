#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField, TextAreaField, HiddenField, SubmitField, BooleanField
from messages import msg
from wpcgi.form import getField

class Template(Form):
    title = TextField(msg['contribtracker-title-label'], id='txt-title')
    content = TextAreaField(msg['contribtracker-content-label'], id="txt-content")
    tabStatus = HiddenField(id="tab-active", validators=[v.IgnoreMe()])
    proceed = SubmitField(msg['contribtracker-button-submit'])
    markup = BooleanField(msg['contribtracker-markup-label'])

def getForm():
    return getField(Template)