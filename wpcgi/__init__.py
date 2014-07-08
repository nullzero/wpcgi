#!/data/project/nullzerobot/python/bin/python

import os

# since the app has no patch, we can still use the old one here
from flask import Flask
app = Flask(__name__)

import site
site.addsitedir("/data/project/nullzerobot/wprobot")
site.addsitedir(os.path.dirname(__file__))

os.environ["WPROBOT_BOT"] = "Nullzerobot"
import wprobot

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
    {
        'name': 'contribtracker',
    },
    # {
    #     'name': 'letstranslate',
    # },
]