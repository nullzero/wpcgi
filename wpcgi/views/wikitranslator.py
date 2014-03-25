#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request
from decorators import langswitch
from models import WikiTranslator
from utils import get_params
from normalize import normalize_url, normalize
from forms.wikitranslator import WikiTranslatorFormCreator
import c

wikitranslator = Blueprint('wikitranslator', __name__, url_prefix='/tools/wikitranslator')

@wikitranslator.route('/')
@wikitranslator.route('/<siteDest>/<siteSource>')
@wikitranslator.route('/<siteDest>/<siteSource>/<title>')
@langswitch
@normalize_url(['title'])
def index(**kwargs):
    normalize(['title'], kwargs)
    if not request.form.get('tabStatus', False):
        if kwargs.get('siteDest', False) and not kwargs.get('title', False):
            kwargs['tabStatus'] = 'content'
        else:
            kwargs['tabStatus'] = 'page'

    if not request.form.get('siteDest', False) and not request.form.get('siteSource', False):
        kwargs['siteDest'] = 'th'
        kwargs['siteSource'] = 'en'

    form = WikiTranslatorFormCreator()(request.form, **kwargs)
    data = WikiTranslator(form)
    if form.validate(data):
        data.render()
    return render('wikitranslator_index.html',
                  tool=__name__,
                  form=form,
                  data=data)

@wikitranslator.route('/submit')
def submit():
    active = request.form.get('tabStatus')
    params = ['siteDest', 'siteSource']
    if active == 'page':
        params.append('title')
    return redirect(url_for('.index', **get_params(params)), code=c.REQUEST)