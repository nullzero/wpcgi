#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

import imp
import os
from collections import defaultdict
from markdown import markdown
from wpcgi import app
import i18n

class Message(object):
    def __init__(self):
        self.messages = defaultdict(dict)
        self.lang = app.config['LANG']
        for name in os.listdir(os.path.join(os.path.dirname(__file__), 'tools')):
            directory = os.path.join(os.path.dirname(__file__), 'tools', name)
            if os.path.isdir(directory):
                file = os.path.join(directory, 'i18n.py')
                msg_mod = imp.load_source(file[:-3], file)
                for lang in msg_mod.messages:
                    self.messages[lang].update(msg_mod.messages[lang])

        for lang in i18n.messages:
            self.messages[lang].update(i18n.messages[lang])

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
