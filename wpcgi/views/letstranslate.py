#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from utils import get_params, newtry
from normalize import normalize_url, normalize
from forms.letstranslate import LetsTranslateFormCreator
from models import LetsTranslate
from messages import msg
from database.letstranslate import STATUS
import c

letstranslate = Blueprint('letstranslate', __name__,
                          url_prefix='/tools/letstranslate')
@letstranslate.route('/')
@langswitch
def index():
    return render('letstranslate_index.html', tool=__name__)

@letstranslate.route('/get_article')
@langswitch
def getarticle():
    return render('letstranslate_get_article.html', tool=__name__)

@letstranslate.route('/<mode>')
@langswitch
def list(mode):
    data = LetsTranslate(mode=mode)
    data.getList()
    return render('letstranslate_list.html',
                  tool=__name__,
                  data=data,
                  mode=mode)

@letstranslate.route('/new')
@letstranslate.route('/<mode>/<rid>')
@langswitch
def edit(mode=None, rid=None):
    additional = {}
    suppress_flash = False
    if mode == 'translated':
        file = 'letstranslate_edit_translated.html'
        nextstep = '.edit'
        nextstepdict = {
            'mode': 'reserved',
            'rid': rid
        }
    elif mode == 'reserved':
        file = 'letstranslate_edit_reserved.html'
        nextstep = '.index'
        nextstepdict = {}
    elif mode == 'final' or mode == 'rejected' or mode == 'done':
        file = 'letstranslate_edit_final.html'
        nextstep = '.list'
        nextstepdict = {
            'mode': mode
        }
        if mode == 'rejected' or mode == 'done':
            suppress_flash = True
    elif mode is None and rid is None:
        file = 'letstranslate_new.html'
        mode = 'new'
        nextstep = '.index'
        nextstepdict = {}

        if not request.form.get('lang', False):
            additional['lang'] = 'en'

    form = LetsTranslateFormCreator(mode=mode)(request.form, **additional)
    data = LetsTranslate(form, rid=rid, mode=mode)

    if not form.validate(data):
        fun = lambda: data.renderEdit()
        onSuccess = lambda _: render(file, tool=__name__, form=form, data=data, mode=mode, status=STATUS)
        onFail = lambda: redirect(url_for('.index'))
    else:
        fun = lambda: data.save()
        def onSuccess(_):
            if not suppress_flash:
                flash(msg['letstranslate-save-success'], 'success')
            return redirect(url_for(nextstep, **nextstepdict))
        onFail = lambda: redirect(url_for('.index'))

    return newtry(locals())

@letstranslate.route('/reject/<mode>/<rid>')
@langswitch
def reject(mode, rid):
    data = LetsTranslate(rid=rid, mode=mode)

    fun = lambda: data.reject()
    def onSuccess(_):
        flash(msg['letstranslate-reject-success'], 'success')
        return redirect(url_for('.list', mode=mode))
    onFail = lambda: redirect(url_for('.index'))

    return newtry(locals())

@letstranslate.route('/recover/<rid>')
@langswitch
def recover(rid):
    data = LetsTranslate(rid=rid)

    fun = lambda: data.recover()
    def onSuccess(_):
        flash(msg['letstranslate-recover-success'], 'success')
        return redirect(url_for('.list', mode='rejected'))
    onFail = lambda: redirect(url_for('.index'))

    return newtry(locals())
