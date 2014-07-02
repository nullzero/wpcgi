#!/data/project/nullzerobot/python/bin/python

from p_form import Form, c_validators as v
from wtforms import TextField, TextAreaField, BooleanField
from wtforms.widgets import SubmitInput
from messages import msg
from forms import getField

class Template(Form):
    pid = TextField(msg['letstranslate-pid-label'], id='txt-pid', validators=[v.Required(), v.Number()])
    name = TextField(msg['letstranslate-name-label'], id='txt-name', validators=[v.Required()])
    name2 = TextField(msg['letstranslate-name2-label'], id='txt-name', validators=[v.Required()])
    lang = TextField(msg['letstranslate-lang-label'], id='txt-lang', validators=[v.Required(), v.IgnoreMe()])
    title = TextField(msg['letstranslate-title-label'], id='txt-title', validators=[v.Required()])
    email = TextField(msg['letstranslate-email-label'], id='txt-email', validators=[v.Required(), v.Email()])
    content = TextAreaField(msg['letstranslate-content-label'], validators=[v.Required()])
    content2 = TextAreaField(msg['letstranslate-content2-label'], validators=[v.Required()])
    wikiuser = BooleanField(msg['letstranslate-wikiuser-label'])

def LetsTranslateFormCreator(mode):
    if mode == 'new':
        field = ['pid', 'name', 'lang', 'title', 'email', 'content', 'wikiuser']
    elif mode == 'translated':
        field = ['name', 'name2', 'lang', 'title', 'email', 'content', 'wikiuser']
    elif mode == 'reserved':
        field = ['name', 'name2', 'lang', 'title', 'email', 'content', 'content2']
    elif mode == 'final' or mode == 'done' or mode == 'rejected':
        field = ['pid', 'name', 'name2', 'lang', 'title', 'email', 'content', 'content2']

    return getField(Template, field)
