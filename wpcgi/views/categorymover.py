#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from models import CategoryMover
from utils import get_params, newtry
from normalize import normalize_url, normalize
from forms import CategoryMoverFormCreator
from messages import msg
import c

categorymover = Blueprint('categorymover', __name__,
                          url_prefix='/tools/categorymover')

@categorymover.route('/')
@categorymover.route('/queue')
@langswitch
def queue(**kwargs):
    data = CategoryMover()
    data.getQueue()
    return render('categorymover_list.html',
                  tool=__name__,
                  data=data,
                  mode='queue')

@categorymover.route('/archive')
@categorymover.route('/archive/<page>')
@langswitch
def archive(page=None):
    data = CategoryMover()
    data.getArchive()
    return render('categorymover_list.html',
                  tool=__name__,
                  data=data,
                  mode='archive')

def calling():
    print locals()

@categorymover.route('/new')
@categorymover.route('/edit/<rid>')
@categorymover.route('/submit/<rid>/<status>')
@langswitch
def edit(rid=None, status=None):
    form = CategoryMoverFormCreator()(request.form)
    data = CategoryMover(form)
    if rid == 'new':
        rid = None
    if status is None or not form.validate(data):
        fun = lambda: data.renderEdit(rid)
        onSuccess = lambda _: render('categorymover_edit.html',
                                     tool=__name__,
                                     form=form,
                                     data=data)
        onFail = lambda: redirect(url_for('.queue'))
    else:
        assert(status == 'success')

        fun = lambda: data.save(rid)

        def onSuccess(result):
            message = 'categorymover-{0}-success'.format('edit' if rid else 'new')
            flash(msg[message].format(result), 'success')
            return redirect(url_for('.queue'))

        onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())

@categorymover.route('/approve/<rid>')
@langswitch
def approve(rid):
    data = CategoryMover()

    fun = lambda: data.approve(rid)
    onSuccess = lambda _: redirect(url_for('.queue'))
    onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())

@categorymover.route('/reject/<rid>')
@langswitch
def reject(rid):
    data = CategoryMover()

    fun = lambda: data.reject(rid)
    onSuccess = lambda _: redirect(url_for('.queue'))
    onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())