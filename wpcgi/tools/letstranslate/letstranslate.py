#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch, in_group
from utils import get_params
from normalize import normalize_url, normalize
from messages import msg
import form
import c
import wpcgi.errors
from pprint import pprint

letstranslate = Blueprint('letstranslate', __name__,
                          file=__file__, tool=True)

@letstranslate.app_errorhandler(Exception)
def exception(e):
    if isinstance(e, letstranslate.model.IDNotFoundError):
        flash(msg['error-letstranslate-id-not-found'], 'danger')
    elif isinstance(e, letstranslate.model.ModeError):
        flash(msg['error-letstranslate-mode'], 'danger')
    else:
        raise
    return redirect(url_for('.index'))

@letstranslate.route('/')
@langswitch
def index():
    return render('index.html', tool=__name__)

"""
@letstranslate.route('/get_article')
@langswitch
def getarticle():
    return render('letstranslate_get_article.html', tool=__name__)
"""

@langswitch
def list_meta(action, mode):
    data = letstranslate.model.Model(action=action, mode=mode)
    data.getList()
    return render('list.html', tool=__name__, data=data)

@letstranslate.route('/format/<mode>')
@in_group(['*'])
def list_format(mode):
    return list_meta(action='format', mode=mode)

@letstranslate.route('/organize/<mode>')
@in_group(['letstranslate', 'approved'])
def list_organize(mode):
    return list_meta(action='organize', mode=mode)

@letstranslate.route('/translate')
def edit_translate():
    # can use additional because renderEdit() will not load anything
    additional = {}
    if not request.form.get('lang', False):
        additional = {
            'lang': 'en',
            'fam': 'wikipedia'
        }
    next = '.confirm_translate'
    return edit_meta(action='translate', file='edit_translate.html', additional=additional, next=next)

@letstranslate.route('/format/<mode>/<id>')
@in_group(['*'])
def edit_format(mode, id):
    file = 'edit_format_' + mode + '.html'
    kwargs = {}
    additional = {}
    if mode == 'reserve':
        kwargs['next'] = '.edit_format'
        kwargs['nextargs'] = {'mode': 'submit'}
    return edit_meta(action='format', mode=mode, id=id, file=file, additional=additional, **kwargs)

@letstranslate.route('/organize/<mode>/<id>')
@in_group(['letstranslate', 'approved'])
def edit_organize(mode, id):
    if mode == 'rejected' or mode == 'done':
        suppress_flash = True
    else:
        suppress_flash = False
    return edit_meta(
        action='organize',
        mode=mode,
        id=id,
        file='edit_organize.html',
        next='.list_organize',
        nextargs={'mode': mode},
        suppress_flash=suppress_flash
    )

@langswitch
def edit_meta(action, mode=None, file='index.html', id=None, suppress_flash=False, next='.index', nextargs={}, additional={}):
    form = letstranslate.form.getForm(action=action, mode=mode)(request.form, **additional)
    data = letstranslate.model.Model(form=form, action=action, id=id, mode=mode)

    if not form.validate(data):
        data.renderEdit()
        return render(file, tool=__name__, form=form, data=data)
    else:
        id = data.save()
        if next in ['.confirm_translate', '.edit_format']:
            nextargs['id'] = id
        if not suppress_flash:
            flash(msg['letstranslate-save-success'], 'success')
        return redirect(url_for(next, **nextargs))

@letstranslate.route('/translate/<id>')
def confirm_translate(id):
    data = letstranslate.model.Model(action='translate', id=id, mode='result')
    return render('confirm.html', tool=__name__, data=data)

@letstranslate.route('/reject/<mode>/<id>')
@in_group(['*'])
@langswitch
def reject(mode, id):
    data = letstranslate.model.Model(action='reject', id=id, mode=mode)
    data.reject()
    flash(msg['letstranslate-reject-success'], 'success')
    if mode == 'organizer':
        return redirect(url_for('.list_organize', mode='submit'))
    else:
        return redirect(url_for('.list_format', mode='reserve'))

@letstranslate.route('/recover/<id>')
@in_group(['letstranslate', 'approved'])
@langswitch
def recover(id):
    data = letstranslate.model.Model(action='recover', id=id)
    data.recover()
    flash(msg['letstranslate-recover-success'], 'success')
    return redirect(url_for('.list_organize', mode='rejected'))
