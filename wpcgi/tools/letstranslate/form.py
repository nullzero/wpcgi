#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField, TextAreaField, BooleanField
from messages import msg
from wpcgi.form import getField

class Template(Form):
    pid = TextField(id='txt-pid', validators=[v.Required(), v.Number()])
    user_translator = TextField(msg['letstranslate-user_translator-label'], id='txt-user_translator', validators=[v.Required(), v.Wiki()])
    user_formatter = TextField(msg['letstranslate-user_formatter-label'], id='txt-name', validators=[v.Required()])
    lang = TextField(msg['letstranslate-lang-label'], id='txt-lang', validators=[v.Required(), v.IgnoreMe()])
    fam = TextField(msg['letstranslate-fam-label'], id='txt-fam', validators=[v.Required(), v.IgnoreMe()])
    title_untranslated = TextField(msg['letstranslate-title_untranslated-label'], id='txt-title_untranslated', validators=[v.Required()])
    title_translated = TextField(msg['letstranslate-title_translated-label'], id='txt-title_translated', validators=[v.Required()])
    email = TextField(msg['letstranslate-email-label'], id='txt-email', validators=[v.Required(), v.Email()])
    content_translated = TextAreaField(msg['letstranslate-content_translated-label'], validators=[v.Required()])
    content_formatted = TextAreaField(msg['letstranslate-content_formatted-label'], validators=[v.Required()])
    wikiuser = BooleanField()
    length = TextField(msg['letstranslate-length-label'])
    id = TextField(msg['letstranslate-id-label'])
    summary = TextField(msg['letstranslate-summary-label'])

def getForm(action, mode):
    if action == 'translate':
        if mode == 'result':
            field = ['length', 'id']
        else:
            field = ['pid', 'user_translator', 'lang', 'fam',
                     'title_untranslated', 'title_translated',
                     'email', 'content_translated', 'wikiuser']
    elif action == 'format':
        if mode == 'reserve':
            field = ['lang', 'fam', 'title_untranslated', 'title_translated', 'content_translated']
        else:
            field = ['user_translator', 'lang', 'fam',
                     'title_untranslated', 'title_translated',
                     'email', 'content_translated', 'content_formatted']
    else:
        field = ['id', 'length', 'pid', 'user_translator', 'lang', 'fam',
                 'title_untranslated', 'title_translated',
                 'email', 'content_translated', 'content_formatted', 'user_formatter']
        if mode == 'submit':
            field.append('summary')

    return getField(Template, field)
