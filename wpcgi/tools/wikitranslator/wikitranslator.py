#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, g, redirect, url_for, request
from decorators import langswitch
from utils import get_params
from normalize import normalize_url, normalize
import form
import c

wikitranslator = Blueprint('wikitranslator', __name__,
                           file=__file__, tool=True)

@wikitranslator.route('/')
@wikitranslator.route('/<siteDest>/<siteSource>')
@wikitranslator.route('/<siteDest>/<siteSource>/<title>')
@langswitch
@normalize_url(['title'])
def index(**kwargs):
    if request.args.get('submit') is not None:
        active = request.form.get('tabStatus')
        params = ['siteDest', 'siteSource']
        if active == 'page':
            params.append('title')
        return redirect(url_for('.index', **get_params(params)), code=c.REQUEST)

    normalize(['title'], kwargs)
    if not request.form.get('tabStatus', False):
        if kwargs.get('siteDest', False) and not kwargs.get('title', False):
            kwargs['tabStatus'] = 'content'
        else:
            kwargs['tabStatus'] = 'page'

    if not request.form.get('siteDest', False) and not request.form.get('siteSource', False):
        kwargs['siteDest'] = 'th'
        kwargs['siteSource'] = 'en'

    form = wikitranslator.form.getForm()(request.form, **kwargs)
    data = wikitranslator.model.Model(form=form)
    if form.validate(data):
        data.render()
    return render('wikitranslator_index.html',
                  tool=__name__,
                  form=form,
                  data=data)

