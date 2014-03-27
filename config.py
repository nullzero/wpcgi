#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

"""
Note: LANG can't be overwritten, as the value is used in message.py
directly from the class BaseConfig
"""

from wpcgi import FLASK_SECRET_KEY

class BaseConfig(object):
    APP_NAME = 'wpcgi'
    CSRF_ENABLED = False
    DEBUG_LOG = '../error.log'
    LANG = 'th'
    SQL = False
    SECRET_KEY = FLASK_SECRET_KEY

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQL = True

    SCRIPT_NAME = '/~nullzero'

class TestProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SCRIPT_NAME = '/~nullzero'

class ProductionConfig(BaseConfig):
    SQL = True
    DEBUG = False
    TESTING = False

    SCRIPT_NAME = '/nullzerobot'