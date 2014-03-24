#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import imp
import os
from collections import defaultdict
from markdown import markdown
from wpcgi import app
import i18n.core

class Message(object):
    def __init__(self):
        self.messages = defaultdict(dict)
        self.lang = app.config['LANG']
        for file in os.listdir(os.path.dirname(i18n.core.__file__)):
            if file.endswith('__init__.py') or not file.endswith('.py'):
                continue
            msg_mod = imp.load_source("msg_mod", os.path.dirname(i18n.core.__file__) + '/' + file)
            for lang in msg_mod.messages:
                self.messages[lang].update(msg_mod.messages[lang])

        for lang in i18n.core.messages:
            self.messages[lang].update(i18n.core.messages[lang])

    def switch_language(self, lang):
        if lang in self.messages:
            self.lang = lang
            return True
        return False

    def __getitem__(self, name):
        if name in self.messages[self.lang]:
            if isinstance(self.messages[self.lang][name], tuple):
                if self.messages[self.lang][name][1] == 'markdown':
                    return markdown(self.messages[self.lang][name][0])
                else:
                    raise Exception('Not support this model of text yet')
            else:
                return self.messages[self.lang][name]
        else:
            return name

msg = Message()