#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from config import BaseConfig

class Message(object):
    def __init__(self):
        self.messages = {}
        self.lang = BaseConfig.LANG

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

from i18n import core, dykchecker, wikitranslator
print msg.messages.keys()