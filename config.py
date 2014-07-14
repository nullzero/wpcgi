#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

"""
Note: LANG can't be overwritten, as the value is used in message.py
directly from the class BaseConfig
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.expanduser('~/.wpcgi.cnf'), 'r') as f:
    key = f.read().split('\n')

class BaseConfig(object):
    APP_NAME = 'wpcgi'
    CSRF_ENABLED = False
    DEBUG_LOG = '../error.log'
    LANG = 'th'
    SQL = True
    SECRET_KEY = key[0][len('secret: '):]
    CONSUMER_KEY = key[1][len('cons_key: '):]
    CONSUMER_SECRET = key[2][len('cons_secret: '):]
    SQLALCHEMY_DATABASE_URI = 'mysql://tools-db/s51093__tools?read_default_file=~/replica.my.cnf'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_POOL_RECYCLE = 3600
    MODE = 'default'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SCRIPT_NAME = '/~nullzero'
    CONSUMER_KEY = key[3][len('cons_key_test: '):]
    CONSUMER_SECRET = key[4][len('cons_secret_test: '):]
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/test'
    MODE = 'test'

class WithoutSQL(TestConfig):
    SQL = False
    MODE = 'nosql'

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    SCRIPT_NAME = '/nullzerobot'
    MODE = 'production'