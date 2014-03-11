#!/data/project/nullzerobot/python/bin/python

from p_form import Form, c_validators as v
from wtforms import TextField, TextAreaField
from wtforms.widgets import SubmitInput
from messages import msg
from models import WikiTranslator

class WikiTranslatorForm(Form):
    pass

def WikiTranslatorFormCreator():
    FormCl = WikiTranslatorForm
    FormCl.title = TextField(msg['wikitranslator-label-title'],
                                 id='txt-title')
    FormCl.siteDest = TextField(msg['wikitranslator-label-siteDest'],
                                validators=[v.Required()])
    FormCl.siteSource = TextField(msg['wikitranslator-label-siteSource'],
                                  validators=[v.Required()])
    FormCl.content = TextAreaField(msg['wikitranslator-label-content'],
                                   id="txt-content")
    return WikiTranslatorForm