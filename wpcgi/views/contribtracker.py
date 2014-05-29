#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from utils import get_params, newtry
from normalize import normalize_url, normalize
from forms.contribtracker import ContribTrackerFormCreator
from models import ContribTracker
from messages import msg
import c

contribtracker = Blueprint('contribtracker', __name__,
                          url_prefix='/tools/contribtracker')
@contribtracker.route('/')
@langswitch
def index():
    return redirect(url_for('.text', mode='page'), code=c.REQUEST)

@contribtracker.route('/user/<user>')
@langswitch
def user(user=None):
    return NotImplemented

@contribtracker.route('/text/<mode>')
@contribtracker.route('/text/<mode>/<path:title>')
@langswitch
def text(**kwargs):
    print kwargs
    if request.args.get('submit') is not None:
        active = request.form.get('tabStatus')
        params = []
        if active == 'page':
            mode = 'page'
            params.append('title')
        else:
            mode = 'content'
        return redirect(url_for('.text', mode=mode, **get_params(params)), code=c.REQUEST)

    if not request.form.get('tabStatus', False):
        if kwargs.get('mode', None) == 'page':
            kwargs['tabStatus'] = 'page'
        else:
            kwargs['tabStatus'] = 'content'

    form = ContribTrackerFormCreator()(request.form, **kwargs)
    data = ContribTracker(form)

    if form.validate(data):
        data.render()
    return render('contribtracker_index.html',
                  tool=__name__,
                  form=form,
                  data=data)
