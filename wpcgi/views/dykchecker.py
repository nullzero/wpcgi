#!/data/project/nullzero/python/bin/python

from p_flask import Blueprint, render_template, g, redirect, url_for, request, current_app
from decorators import langswitch
from forms import DYKCheckerForm
from models import DYKChecker
from utils import get_params
from normalize import normalize_url, normalize
import c

dykchecker = Blueprint('dykchecker', __name__, url_prefix='/tools/dykchecker')

@dykchecker.route('/')
@dykchecker.route('/<title>/')
@dykchecker.route('/<title>/<oldid>/')
@langswitch
@normalize_url(['title'])
def index(**kwargs):
    normalize(['title'], kwargs)
    form = DYKCheckerForm(request.form, **kwargs)
    data = DYKChecker(form)
    if form.validate(data):
        data.render()
        return render_template('dykchecker_page.html',
                               tool=True,
                               title='dykchecker',
                               form=form,
                               data=data)
        
    else:
        return render_template('dykchecker_index.html',
                               tool=True,
                               title='dykchecker',
                               form=form,
                               data=None)

@dykchecker.route('/submit')
def submit():
    return redirect(url_for('.index', **get_params(['title', 'oldid'])), code=c.REQUEST)