#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, current_app
from decorators import langswitch
from models import DYKChecker
from utils import get_params
from normalize import normalize_url, normalize
from forms import DYKCheckerFormCreator
import c

dykchecker = Blueprint('dykchecker', __name__, url_prefix='/tools/dykchecker')

@dykchecker.route('/')
@dykchecker.route('/<title>/')
@dykchecker.route('/<title>/<oldid>/')
@langswitch
@normalize_url(['title'])
def index(**kwargs):
    normalize(['title'], kwargs)
    form = DYKCheckerFormCreator()(request.form, **kwargs)
    data = DYKChecker(form)
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

@dykchecker.route('/submit')
def submit():
    return redirect(url_for('.index', **get_params(['title', 'oldid'])), code=c.REQUEST)