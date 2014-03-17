#!/data/project/nullzerobot/python/bin/python

from p_flask import (Blueprint, render, request,
                   flash, url_for, redirect, session, abort)
from decorators import langswitch

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
@langswitch
def index():
    return render('index.html')

@frontend.route('/tools/')
@langswitch
def alltools():
    return render('alltools.html')

@frontend.route('/about/')
@langswitch
def about():
    return render('about.html')