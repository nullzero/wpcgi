#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

class BaseConfig(object):
    APP_NAME = 'wpcgi'
    CSRF_ENABLED = False
    DEBUG_LOG = '../error.log'
    LANG = "en"
    # os.urandom(24)
    SECRET_KEY = 'you-will-never-guess'
    

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    
    SCRIPT_NAME = '/~nullzero'

class TestProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    
    SCRIPT_NAME = '/~nullzero'

class ProductionConfig(object):
    DEBUG = False
    TESTING = False
    
    SCRIPT_NAME = '/nullzerobot'