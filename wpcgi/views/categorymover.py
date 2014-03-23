#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request
from decorators import langswitch
from models import CategoryMover
from utils import get_params
from normalize import normalize_url, normalize
#from forms import WikiTranslatorFormCreator
import c

categorymover = Blueprint('categorymover', __name__, url_prefix='/tools/categorymover')

@categorymover.route('/')
@categorymover.route('/queue')
@langswitch
def queue(**kwargs):
    #form = WikiTranslatorFormCreator()(request.form, **kwargs)
    data = CategoryMover()
    data.renderQueue()
    return render('categorymover_queue.html',
                  tool=__name__,
                  #form=form,
                  data=data)

"""
@categorymover.route('/submit')
def submit():
    return redirect(url_for('.index', **get_params(['siteDest', 'siteSource', 'title'])), code=c.REQUEST)
"""

@categorymover.route('/new')
@langswitch
def new():
    pass

@categorymover.route('/archive')
@categorymover.route('/archive/<page>')
@langswitch
def archive(page=None):
    pass

@categorymover.route('/delete/<rid>')
@langswitch
def delete(rid):
    pass

@categorymover.route('/edit/<rid>')
@langswitch
def edit(rid):
    pass

@categorymover.route('/approve/<rid>')
@langswitch
def approve(rid):
    return redirect(url_for('.queue'))

@categorymover.route('/reject/<rid>')
@langswitch
def reject(rid):
    data = CategoryMover()
    data.renderReject(rid)
    return redirect(url_for('.queue'))