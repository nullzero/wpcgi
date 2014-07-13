#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, redirect, url_for, request, flash
from decorators import langswitch, in_group
from messages import msg

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
        data.renderEdit()
        return render('edit.html', tool=__name__, form=form, data=data)
    else:
        result = data.save()
        message = 'categorymover-{0}-success'.format('edit' if rid else 'new')
        flash(msg[message].format(result), 'success')
        return redirect(url_for('.queue'))

@in_group(['categorymover', 'approved'])
@categorymover.route('/<mode>/<rid>')
def changeStatus(mode, rid):
    data = categorymover.model.Model(rid=rid)
    data.changeStatus(mode)
    return redirect(url_for('.queue'))