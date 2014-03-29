#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

"""
Note: LANG can't be overwritten, as the value is used in message.py
directly from the class BaseConfig
"""

import os

with open(os.path.expanduser('~/.wpcgi.cnf'), 'r') as f:
    key = f.read().split('\n')

class BaseConfig(object):
    APP_NAME = 'wpcgi'
    CSRF_ENABLED = False
    DEBUG_LOG = '../error.log'
    LANG = 'th'
    SQL = False
    SECRET_KEY = key[0][len('secret: '):]
    CONSUMER_KEY = key[1][len('cons_key: '):]
    CONSUMER_SECRET = key[2][len('cons_secret: '):]

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQL = True

    SCRIPT_NAME = '/~nullzero'
    CONSUMER_KEY = key[3][len('cons_key_test: '):]
    CONSUMER_SECRET = key[4][len('cons_secret_test: '):]

class TestProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SCRIPT_NAME = '/~nullzero'

class ProductionConfig(BaseConfig):
    SQL = True
    DEBUG = False
    TESTING = False

    SCRIPT_NAME = '/nullzerobot'