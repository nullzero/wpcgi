#!/data/project/nullzero/python/bin/python

from p_flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, g, abort)

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/tools/')
def alltools():
    return render_template('alltools.html')