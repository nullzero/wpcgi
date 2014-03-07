#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

class Config(object):
    APP_NAME = 'wpcgi'
    CSRF_ENABLED = False
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'you-will-never-guess'
    LANG = "en"
    DEBUG_LOG = 'error.log'

    # os.urandom(24)
    SECRET_KEY = 'secret key'