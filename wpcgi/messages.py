#!/data/project/nullzero/python/bin/python
# -*- coding: utf-8 -*-

import config

class Message(object):
    def __init__(self):
        self.messages = {}
        self.lang = config.Config.LANG
    
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

msg.messages['en'] = {
    '__NAME__': 'English',
}

msg.messages['th'] = {
    '__NAME__': u'ไทย',
    'dykchecker-page-not-found': u'ไม่พบหน้าดังกล่าว',
    'dykchecker-revision-info': u'ข้อมูลรุ่น',
    'dykchecker-revision-info-value': u'รุ่นล่าสุดคือรุ่น {0} ของหน้า {1} แก้ไขโดย {2} เมื่อ {3} (UTC)',
    'dykchecker-inlineref': u'อ้างอิง',
    'dykchecker-inlineref-value': u'มีอ้างอิงในบรรทัดทั้งหมดจำนวน {0} แห่ง',
    'dykchecker-inlineref-desc': u'ข้อความที่ใช้เสนอบทความรู้ไหมว่าต้องมีอ้างอิงในบรรทัดยืนยันอย่างน้อย 1 แหล่ง',
    'dykchecker-length-value': u'รุ่นล่าสุดมีความยาว {0} อักขระ',
    'dykchecker-length': u'ความยาว',
    'dykchecker-length-desc': u'บทความรู้ไหมว่าต้องมีความยาวของความเรียงอย่างต่ำ 2000 อักขระ',
    'dykchecker-creation-new-desc': u'บทความรู้ไหมว่าต้องสร้างภายใน 14 วัน (ยกเว้นมีการปรับปรุงอย่างมีนัยยะสำคัญ)',
    'dykchecker-creation-desc': u'',
    'dykchecker-old-revision': u'รุ่นเก่า',
    'dykchecker-old-revision-desc': u'ความยาวความเรียงต้องเพิ่มขึ้นอย่างน้อย 2 เท่า ภายในเวลา 14 วัน ยกเว้นเป็นบทความสร้างใหม่',
    'dykchecker-old-revision-not-exist': u'ไม่พบรุ่นเก่าภายในเวลา 14 วัน',
    'dykchecker-old-revision-value': u'รุ่น {0} ซึ่งเป็นรุ่นเก่าเมื่อ {1} UTC ({2} วันที่แล้ว) มีความยาว {3} อักขระ ขณะนี้มีเนื้อหาเพื่มขึ้น {4} เท่า',
    'dykchecker-creation': u'สร้างบทความ',
    'dykchecker-creation-value': u'บทความนี้สร้างโดย {2} เมื่อ {1} ({3} วันที่แล้ว - รุ่น {0})',
    'dykchecker-summary': u'<b>สรุป</b>',
    'dykchecker-summary-fail': u'บทความนี้ไม่ผ่านเกณฑ์บทความรู้ไหมว่า',
    'dykchecker-summary-pass': u'บทความนี้ผ่านเกณฑ์บทความรู้ไหมว่า สามารถ<a style="color: blue" href="//th.wikipedia.org/wiki/วิกิพีเดีย:รู้ไหมว่า/หัวข้อที่ถูกเสนอ">ดำเนินการเสนอ</a>บทความได้',
}

msg.messages['msg'] = {
    '__NAME__': 'Messages',
}