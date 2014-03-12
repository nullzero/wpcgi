#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from p_flask import request

class AttrObject(dict):
    def __init__(self, *args, **kwargs):
        super(AttrObject, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
class DefaultDict(dict):
    def __missing__(self, key):
        return key

def get_params(L):
    dic = {}
    for name in L:
        var = request.form.get(name, None)
        if var:
            dic[name] = var
    return dic