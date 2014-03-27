#!/data/project/nullzerobot/python/bin/python

import os
import sys

sys.path.append(os.path.abspath(os.path.split(__file__)[0]))
sys.path.append(os.path.abspath(os.path.join(os.path.split(__file__)[0], "..")))
os.environ['WPCGI_PATH'] = os.path.abspath(os.path.join(os.path.split(__file__)[0], ".."))
sys.path.append(os.path.abspath(os.path.join(os.path.split(__file__)[0], "package")))

os.environ["WPROBOT_BOT"] = "Nullzerobot"
sys.path.append("/data/project/nullzerobot/wprobot")

import wprobot

from flask import Flask
app = Flask(__name__)

tools = [
    {
        'name': 'dykchecker',
    },
    {
        'name': 'wikitranslator',
    },
    {
        'name': 'categorymover',
        'disabled': True,
    },
]

import os

with open(os.path.expanduser('~/.wpcgi.cnf'), 'r') as f:
    key = f.read().split('\n')

FLASK_SECRET_KEY = key[0][len('secret: '):]
CONSUMER_KEY = key[1][len('cons_key: '):]
CONSUMER_SECRET = key[2][len('cons_secret: '):]

from flask_mwoauth import MWOAuth

mwoauth = MWOAuth(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
app.register_blueprint(mwoauth.bp)