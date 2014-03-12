#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, current_app
from decorators import langswitch
from models import WikiTranslator
from utils import get_params
from normalize import normalize_url, normalize
from forms import WikiTranslatorFormCreator
import c

wikitranslator = Blueprint('wikitranslator', __name__, url_prefix='/tools/wikitranslator')

@wikitranslator.route('/')
@wikitranslator.route('/<siteDest>/<siteSource>/<title>')
@langswitch
@normalize_url(['title'])
def index(**kwargs):
    normalize(['title'], kwargs)
    form = WikiTranslatorFormCreator()(request.form, **kwargs)
    data = WikiTranslator(form, tabactive=request.form.get('tab-active', None))
    if form.validate(data):
        data.render()
    return render('wikitranslator_index.html',
                  tool=__name__,
                  form=form,
                  data=data)
                  
@wikitranslator.route('/submit')
def submit():
    return redirect(url_for('.index', **get_params(['siteDest', 'siteSource', 'title'])), code=c.REQUEST)