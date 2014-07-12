#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField
from messages import msg
from wpcgi.form import getField

class Template(Form):
    fam = TextField(msg['categorymover-fam-label'], id='txt-fam', validators=[v.Required()])
    lang = TextField(msg['categorymover-lang-label'], id='txt-lang', validators=[v.Required()])
    cat_from = TextField(msg['categorymover-cat_from-label'], id='txt-cat_from', validators=[v.Required()])
    cat_to = TextField(msg['categorymover-cat_to-label'], id='txt-cat_to', validators=[v.Required()])
    note = TextField(msg['categorymover-note-label'])

def getForm():
    return getField(Template)