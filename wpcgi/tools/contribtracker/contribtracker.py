#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, redirect, url_for, request
from decorators import langswitch
from utils import get_params
import c

contribtracker = Blueprint('contribtracker', __name__,
                           file=__file__, tool=True)
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

    form = contribtracker.form.getForm()(request.form, **kwargs)
    data = contribtracker.model.Model(form=form)

    if form.validate(data):
        data.render()
    return render('index.html',
                  tool=__name__,
                  form=form,
                  data=data)
