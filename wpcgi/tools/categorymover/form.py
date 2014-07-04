#!/data/project/nullzerobot/python/bin/python

from flask.ext.wtf import Form
import wtforms.validators as v
from wtforms import TextField
from wtforms.widgets import SubmitInput
from messages import msg

class CategoryMoverForm(Form):
    pass

def form():
    FormCl = CategoryMoverForm
    FormCl.fam = TextField(msg['categorymover-fam-label'], id='txt-fam', validators=[v.Required()])
    FormCl.lang = TextField(msg['categorymover-lang-label'], id='txt-lang', validators=[v.Required()])
    FormCl.catfrom = TextField(msg['categorymover-catfrom-label'], id='txt-catfrom', validators=[v.Required()])
    FormCl.catto = TextField(msg['categorymover-catto-label'], id='txt-catto', validators=[v.Required()])
    FormCl.note = TextField(msg['categorymover-note-label'])
    return FormCl