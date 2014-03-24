#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from models import CategoryMover
from utils import get_params, newtry
from normalize import normalize_url, normalize
from forms import CategoryMoverFormCreator
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
        return newtry(
            fn=lambda: data.renderEdit(rid),
            success=lambda: render(
                'categorymover_edit.html',
                tool=__name__,
                form=form,
                data=data,
            ),
            fail=lambda: redirect(url_for('.queue')),
        )
    else:
        assert(status == 'success')
        return newtry(fn=lambda: data.save(rid),
                      success=lambda: redirect(url_for('.queue')),
                      fail=lambda: redirect(url_for('.queue')))

@categorymover.route('/approve/<rid>')
@langswitch
def approve(rid):
    data = CategoryMover()
    return newtry(
        fn=lambda: data.approve(rid),
        success=lambda: redirect(url_for('.queue')),
        fail=lambda: redirect(url_for('.queue'))
    )

@categorymover.route('/reject/<rid>')
@langswitch
def reject(rid):
    data = CategoryMover()
    return newtry(
        fn=lambda: data.reject(rid),
        success=lambda: redirect(url_for('.queue')),
        fail=lambda: redirect(url_for('.queue'))
    )
