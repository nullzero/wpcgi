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