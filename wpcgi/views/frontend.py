#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render
from decorators import langswitch
from wpcgi import tools

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
@langswitch
def index():
    return render('index.html')

@frontend.route('/tools/')
@langswitch
def alltools():
    return render('alltools.html', tools=tools)

@frontend.route('/about/')
@langswitch
def about():
    return render('about.html')

@frontend.route('/faq/')
@langswitch
def faq():
    return render('faq.html')
