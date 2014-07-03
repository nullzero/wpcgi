#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from models import CategoryMover
from utils import get_params, newtry
from normalize import normalize_url, normalize
from forms.categorymover import CategoryMoverFormCreator
from messages import msg
import c

categorymover = Blueprint('categorymover', __name__,
                          url_prefix='/tools/categorymover')

@categorymover.route('/', endpoint='index')
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

@categorymover.route('/new')
@categorymover.route('/edit/<rid>')
@langswitch
def edit(rid=None):
    form = CategoryMoverFormCreator()(request.form)
    data = CategoryMover(form, rid)

    if not form.validate(data):
        fun = lambda: data.renderEdit()
        onSuccess = lambda _: render('categorymover_edit.html',
                                     tool=__name__,
                                     form=form,
                                     data=data)
        onFail = lambda: redirect(url_for('.queue'))
    else:
        fun = lambda: data.save()

        def onSuccess(result):
            message = 'categorymover-{0}-success'.format('edit' if rid else 'new')
            flash(msg[message].format(result), 'success')
            return redirect(url_for('.queue'))

        onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())

@categorymover.route('/approve/<rid>')
@langswitch
def approve(rid):
    data = CategoryMover(rid)

    fun = lambda: data.approve()
    onSuccess = lambda _: redirect(url_for('.queue'))
    onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())

@categorymover.route('/reject/<rid>')
@langswitch
def reject(rid):
    data = CategoryMover(rid)

    fun = lambda: data.reject()
    onSuccess = lambda _: redirect(url_for('.queue'))
    onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())