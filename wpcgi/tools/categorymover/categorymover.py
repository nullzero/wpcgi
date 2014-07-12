#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from utils import get_params, newtry
from normalize import normalize_url, normalize
from messages import msg
import form
import c

categorymover = Blueprint('categorymover', __name__,
                          file=__file__, tool=True)

@categorymover.route('/', endpoint='index')
@categorymover.route('/queue')
@langswitch
def queue():
    data = categorymover.model.Model()
    data.getQueue()
    return render('list.html',
                  tool=__name__,
                  data=data,
                  mode='queue')

@categorymover.route('/archive')
@categorymover.route('/archive/<page>')
@langswitch
def archive(page=None):
    data = categorymover.model.Model()
    data.getArchive()
    return render('list.html',
                  tool=__name__,
                  data=data,
                  mode='archive')

@categorymover.route('/new')
@categorymover.route('/edit/<rid>')
@langswitch
def edit(rid=None):
    form = categorymover.form.getForm()(request.form)
    data = categorymover.model.Model(form=form, rid=rid)

    if not form.validate(data):
        fun = lambda: data.renderEdit()
        onSuccess = lambda _: render('edit.html',
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
def approve(rid):
    print '>>>', rid
    data = categorymover.model.Model(rid=rid)

    fun = lambda: data.approve()
    onSuccess = lambda _: redirect(url_for('.queue'))
    onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())

@categorymover.route('/reject/<rid>')
def reject(rid):
    data = categorymover.model.Model(rid=rid)

    fun = lambda: data.reject()
    onSuccess = lambda _: redirect(url_for('.queue'))
    onFail = lambda: redirect(url_for('.queue'))

    return newtry(locals())
