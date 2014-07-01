#!/data/project/nullzerobot/python/bin/python

from p_form import Form, c_validators as v
from wtforms import TextField, TextAreaField, BooleanField
from wtforms.widgets import SubmitInput
from messages import msg
from forms import getField

class Template(Form):
    pid = TextField(msg['letstranslate-pid-label'], id='txt-pid', validators=[v.Required()])
    name = TextField(msg['letstranslate-name-label'], id='txt-name', validators=[v.Required()])
    name2 = TextField(msg['letstranslate-name-label'], id='txt-name', validators=[v.Required()])
    lang = TextField(msg['letstranslate-lang-label'], id='txt-lang', validators=[v.Required()])
    title = TextField(msg['letstranslate-title-label'], id='txt-title', validators=[v.Required()])
    email = TextField(msg['letstranslate-email-label'], id='txt-email', validators=[v.Required()])
    content = TextAreaField(msg['letstranslate-note-label'])
    content2 = TextAreaField(msg['letstranslate-note-label'])
    wikiuser = BooleanField(msg['letstranslate-wikiuser-label'])
    stop = TextField('', validators=[v.Required()])

def LetsTranslateFormCreator(mode):
    if mode == 'new':
        field = ['pid', 'name', 'lang', 'title', 'email', 'content', 'wikiuser']
    elif mode == 'translated':
        field = ['name', 'name2', 'lang', 'title', 'email', 'content', 'wikiuser']
    elif mode == 'reserved':
        field = ['name', 'name2', 'lang', 'title', 'email', 'content', 'content2']
    elif mode == 'final':
        field = ['pid', 'name', 'name2', 'lang', 'title', 'email', 'content', 'content2', 'stop']

    return getField(Template, field)
