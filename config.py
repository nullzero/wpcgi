#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

"""
Note: LANG can't be overwritten, as the value is used in message.py
directly from the class BaseConfig
"""

class BaseConfig(object):
    APP_NAME = 'wpcgi'
    CSRF_ENABLED = False
    DEBUG_LOG = '../error.log'
    LANG = 'th'
    SQL = False
    # os.urandom(24)
    SECRET_KEY = 'you-will-never-guess'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    #SQL = True

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