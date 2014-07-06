#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField, TextAreaField, HiddenField, SubmitField
from messages import msg
from models import WikiTranslator

class WikiTranslatorForm(Form):
    pass

def getForm():
    FormCl = WikiTranslatorForm
    FormCl.title = TextField(msg['wikitranslator-title-label'],
                                 id='txt-title')
    FormCl.siteDest = TextField(msg['wikitranslator-siteDest-label'],
                                id='txt-siteDest',
                                validators=[v.Required(), v.IgnoreMe()])
    FormCl.siteSource = TextField(msg['wikitranslator-siteSource-label'],
                                  id='txt-siteSource',
                                  validators=[v.Required(), v.IgnoreMe()])
    FormCl.content = TextAreaField(msg['wikitranslator-content-label'],
                                   id="txt-content")
    FormCl.tabStatus = HiddenField(id="tab-active", validators=[v.IgnoreMe()])
    FormCl.proceed = SubmitField(msg['wikitranslator-button-submit'])
    return FormCl