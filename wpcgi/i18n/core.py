#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from messages import msg

msg.messages['en'] = {
    '__NAME__': 'English',
}

msg.messages['th'] = {
    '__NAME__': u'ไทย',
    'core-name': u'เครื่องมือของ Nullzero',
    'core-page-generated': u'หน้านี้สร้างใน {0} วินาที',
    'core-required-symbol': u'*',
    'core-encounter-error': u'หากพบข้อผิดพลาด โปรดติดต่อ'
                            u'<a href="//th.wikipedia.org/wiki/User_talk:Nullzero">ผู้ดูแลเครื่องมือ</a>',

    'toolbar-home': u'หน้าหลัก',
    'toolbar-tools': u'เครื่องมือทั้งหมด',
    'toolbar-status-of-bot': u'สถานะของบอต',
    'toolbar-contact': u'ติดต่อ',
    'toolbar-about': u'เกี่ยวกับ',
    
    'validator-require': u'ต้องกรอกช่องนี้',
    'validator-not-number': u'ต้องเป็นตัวเลข',
}

msg.messages['msg'] = {
    '__NAME__': 'Messages',
}