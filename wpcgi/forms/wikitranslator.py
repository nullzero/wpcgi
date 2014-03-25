#!/data/project/nullzerobot/python/bin/python

from p_form import Form, c_validators as v
from wtforms import TextField, TextAreaField, HiddenField, SubmitField
from messages import msg
from models import WikiTranslator
from forms import lang_default

class WikiTranslatorForm(Form):
    pass

def WikiTranslatorFormCreator():
    FormCl = WikiTranslatorForm
    FormCl.title = TextField(msg['wikitranslator-title-label'],
                                 id='txt-title')
    FormCl.siteDest = lang_default(msg['wikitranslator-siteDest-label'],
                                   id='txt-siteDest',
                                   validators=[v.Required()])
    FormCl.siteSource = lang_default(msg['wikitranslator-siteSource-label'],
                                     id='txt-siteSource',
                                     validators=[v.Required()])
    FormCl.content = TextAreaField(msg['wikitranslator-content-label'],
                                   id="txt-content")
    FormCl.tabStatus = HiddenField(id="tab-active", validators=[v.IgnoreMe()])
    FormCl.proceed = SubmitField(msg['wikitranslator-button-submit'])
    return FormCl