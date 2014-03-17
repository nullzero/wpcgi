#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import imp
import os
from collections import defaultdict
from wpcgi import app

class Message(object):
    def __init__(self):
        self.messages = defaultdict(dict)
        self.lang = app.config['LANG']
        import i18n.core
        for file in os.listdir(os.path.dirname(i18n.core.__file__)):
            if file.endswith('__init__.py') or not file.endswith('.py'):
                continue
            msg_mod = imp.load_source("msg_mod", os.path.dirname(i18n.core.__file__) + '/' + file)
            for lang in msg_mod.messages:
                self.messages[lang].update(msg_mod.messages[lang])

    def switch_language(self, lang):
        if lang in self.messages:
            self.lang = lang
            return True
        return False

    def __getitem__(self, name):
        if name in self.messages[self.lang]:
            return self.messages[self.lang][name]
        else:
            return name

msg = Message()