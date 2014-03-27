#!/data/project/nullzerobot/python/bin/python

from p_flask import (Blueprint, render, request,
                   flash, url_for, redirect, session, abort)
from decorators import langswitch
from wpcgi import tools, app, mwoauth

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
@langswitch
def index():
    return "logged in as: " + repr(mwoauth.get_current_user(False)) + "<br>" + \
               "<a href=login>login</a> / <a href=logout>logout</a>"
    #return render('index.html')

@frontend.route('/tools/')
@langswitch
def alltools():
    return render('alltools.html', tools=tools)

@frontend.route('/about/')
@langswitch
def about():
    return render('about.html')