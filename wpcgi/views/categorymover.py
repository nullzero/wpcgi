#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request
from decorators import langswitch
from models import CategoryMover
from utils import get_params
from normalize import normalize_url, normalize
from forms import CategoryMoverFormCreator
import c

categorymover = Blueprint('categorymover', __name__, url_prefix='/tools/categorymover')

@categorymover.route('/')
@categorymover.route('/queue')
@langswitch
def queue(**kwargs):
    return render('categorymover_queue.html',
                  tool=__name__,
                  data=CategoryMover())

@categorymover.route('/new')
@categorymover.route('/edit/<rid>')
@langswitch
def edit(rid=None):
    form = CategoryMoverFormCreator()(request.form)
    data = CategoryMover(form)
    data.renderEdit(rid)
    if form.validate(data):
        data.save()
        return redirect(url_for('.queue'))
    else:
        return render('categorymover_edit.html',
                      tool=__name__,
                      form=form,
                      data=data)

@categorymover.route('/archive')
@categorymover.route('/archive/<page>')
@langswitch
def archive(page=None):
    pass

@categorymover.route('/delete/<rid>')
@langswitch
def delete(rid):
    pass

@categorymover.route('/approve/<rid>')
@langswitch
def approve(rid):
    data = CategoryMover()
    data.approve(rid)
    return redirect(url_for('.queue'))

@categorymover.route('/reject/<rid>')
@langswitch
def reject(rid):
    data = CategoryMover()
    data.reject(rid)
    return redirect(url_for('.queue'))