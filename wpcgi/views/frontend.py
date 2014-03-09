#!/data/project/nullzerobot/python/bin/python

from p_flask import (Blueprint, render, current_app, request,
                   flash, url_for, redirect, session, g, abort)

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render('index.html')

@frontend.route('/tools/')
def alltools():
    return render('alltools.html')