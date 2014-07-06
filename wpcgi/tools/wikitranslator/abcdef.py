#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

messages = {}

messages['th'] = {
    'wikitranslator-title': u'เครื่องมือแปลลิงก์วิกิพีเดีย',
    'wikitranslator-description': u'เครื่องมือแปลลิงก์ในหน้าวิกิพีเดียรวมไปถึงแม่แบบและหมวดหมู่ โดยนำข้อมูลมาจากลิงก์ข้ามภาษา',
    'wikitranslator-siteDest-label': u'ไซต์ปลายทาง',
    'wikitranslator-siteSource-label': u'ไซต์ต้นทาง',
    'wikitranslator-disclaimer': u'(โปรดทราบว่าวิกิพีเดียภาษาไทยไม่รับบทความภาษาต่างประเทศ '
                                 u'บทความที่แปลผ่านเครื่องมือนี้และไม่มีการแปลเพิ่มเติมจนเป็นภาษาไทยทั้งหมด'
                                 u'จะถูกลบอย่างแน่นอนหากส่งเข้าเนมสเปซหลัก)',
    'wikitranslator-title-label': u'ชื่อหน้า',
    'wikitranslator-title-placeholder': u'เช่น "A"',
    'wikitranslator-content-label': u'ข้อความ',
    'wikitranslator-content-placeholder': u'เช่น "[[C++]] is a [[programming language]]{{cn}}."',

    'wikitranslator-button-submit': u'แปล!',
    'wikitranslator-button-save': u'บันทึก',

    'wikitranslator-tab-page': u'ใช้ชื่อหน้า',
    'wikitranslator-tab-content': u'ใช้ข้อความ',

    'wikitranslator-exempt-tag': u'บทความคัดสรร|บทความคุณภาพ|ล็อก|กึ่งล็อก',
    'wikitranslator-exempt-notice': (u'หมายเหตุ: นี่คือแม่แบบที่ใช้ติดแสดงสถานะของหน้าในวิกิพีเดียที่แปลมาวิกิพีเดียภาษาอื่น '
                                     u'ซึ่งหน้าในวิกิพีเดียปลายทางอาจจะไม่ได้มีสถานะเช่นนั้น'),
}

messages['en'] = {
    'wikitranslator-title': u'WikiTranslator',
    'wikitranslator-description': ('a tool to translate links in pages, including template links and category links, '
                                   'based on interlanguage links'),
    'wikitranslator-siteDest-label': u'Destination',
    'wikitranslator-siteSource-label': u'Source',
    'wikitranslator-disclaimer': ('(Please be informed that publishing translated articles from this tool '
                                  'without additional translating to main namespace will result in article deletion.'),
    'wikitranslator-title-label': u'Page title',
    'wikitranslator-title-placeholder': u'e.g. A',
    'wikitranslator-content-label': u'Content',
    'wikitranslator-content-placeholder': u'e.g. "[[ภาษาซีพลัสพลัส]] เป็น [[ภาษาโปรแกรม]]{{ต้องการอ้างอิงเฉพาะส่วน}}."',

    'wikitranslator-button-submit': u'Translate',
    'wikitranslator-button-save': u'Save',

    'wikitranslator-tab-page': u'Use title',
    'wikitranslator-tab-content': u'Use content',

    'wikitranslator-exempt-tag': u'featured article|good article|pp',
    'wikitranslator-exempt-notice': ('Note: this is a tag showing status of a page. '
                                     'Since this tag is translated from the source, it might not reflect the actual status '
                                     'of this page in the destination; you might want to consider to delete it'),
}