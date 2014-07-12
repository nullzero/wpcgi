#!/data/project/nullzerobot/python/bin/python

from messages import msg

REQUEST = 307

FORM_ALLLANGS = [(lang, msg['form-lang-' + lang]) for lang in [
    'th', 'en',
    # 'de', 'fr', 'it', 'ru', 'vi', 'zh'
]]

FORM_ALLFAMS = [(lang, msg['form-fam-' + lang]) for lang in [
    'wikipedia', 'wikibooks'
]]