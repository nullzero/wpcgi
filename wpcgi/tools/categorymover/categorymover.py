#!/data/project/nullzerobot/python/bin/python

from flask import Blueprint, render, g, redirect, url_for, request, flash
from decorators import langswitch
from utils import get_params, newtry
from normalize import normalize_url, normalize
from messages import msg
import form
import c

categorymover = Blueprint('categorymover', __name__,
                          file=__file__, tool=True)

@categorymover.route('/', endpoint='index')
@categorymover.route('/queue')
@langswitch
def queue():
    model = categorymover.model.Model()
    return '123'
