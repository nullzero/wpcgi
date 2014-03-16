#!/data/project/nullzerobot/python/bin/python

from p_flask import Blueprint, render, g, redirect, url_for, request, current_app
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
    #if form.validate(data):
    #    data.render()
    return render('categorymover_index.html',
                  tool=__name__,
                  #form=form,
                  data=data,
                  )

@categorymover.route('/submit')
def submit():
    return redirect(url_for('.index', **get_params(['siteDest', 'siteSource', 'title'])), code=c.REQUEST)

@categorymover.route('/new')
@langswitch
def new():
    pass

@categorymover.route('/archive')
@categorymover.route('/archive/<page>')
@langswitch
def list(page=None):
    pass

@categorymover.route('/delete/<page>')
@langswitch
def delete(page):
    pass

@categorymover.route('/edit/<page>')
@langswitch
def edit(page):
    pass