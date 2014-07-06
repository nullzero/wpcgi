#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, g, redirect, url_for, request
from decorators import langswitch
from utils import get_params
from normalize import normalize_url, normalize
import form
import c

dykchecker = Blueprint('dykchecker', __name__,
                       file=__file__, tool=True)

@dykchecker.route('/')
@dykchecker.route('/<title>/')
@dykchecker.route('/<title>/<oldid>/')
@langswitch
@normalize_url(['title'])
def index(**kwargs):
    if request.args.get('submit') is not None:
        return redirect(url_for('.index', **get_params(['title', 'oldid'])), code=c.REQUEST)

    normalize(['title'], kwargs)
    form = dykchecker.form.getForm()(request.form, **kwargs)
    data = dykchecker.model.Model(form)
    if form.validate(data):
        data.render()
        return render('dykchecker_page.html',
                      tool=__name__,
                      form=form,
                      data=data)

    else:
        return render('dykchecker_index.html',
                      tool=__name__,
                      form=form)
