#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from utils import get_params, newtry
from normalize import normalize_url, normalize
from forms.letstranslate import LetsTranslateFormCreator
from models import LetsTranslate
from messages import msg
import c

letstranslate = Blueprint('letstranslate', __name__,
                          url_prefix='/tools/letstranslate')
@letstranslate.route('/')
@langswitch
def index():
    return render('letstranslate_index.html')

@letstranslate.route('/get_article')
@langswitch
def getarticle():
    return render('letstranslate_get_article.html')

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
    elif mode == 'final':
        file = 'letstranslate_edit_final.html'
    elif mode is None and rid is None:
        file = 'letstranslate_new.html'
        mode = 'new'
        nextstep = '.index'
        nextstepdict = {}

    form = LetsTranslateFormCreator(mode=mode)(request.form)
    data = LetsTranslate(form, rid=rid, mode=mode)

    if not form.validate(data):
        fun = lambda: data.renderEdit()
        onSuccess = lambda _: render(file, tool=__name__, form=form, data=data)
        onFail = lambda: redirect(url_for('.index'))
    else:
        fun = lambda: data.save()
        def onSuccess(_):
            flash(msg['letstranslate-save-success'], 'success')
            return redirect(url_for(nextstep, **nextstepdict))
        onFail = lambda: redirect(url_for('.index'))

    return newtry(locals())

@letstranslate.route('/reject/<mode>/<rid>')
@langswitch
def reject(mode, rid):
    return render('letstranslate_index.html')
