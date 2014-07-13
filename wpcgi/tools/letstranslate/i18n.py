#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

messages = {}

messages['th'] = {
    'letstranslate-title': u'แปลกันเถอะ!',
    'letstranslate-description-content': (
        u'''
### สำหรับพนักงาน DTAC (ผู้แปล)
โปรดคลิก "ส่งการแปลบทความ" กรอกข้อมูลเกี่ยวกับบทความที่คุณแปล เนื้อหาที่แปลแล้ว จากนั้นกด "ตกลง"

### สำหรับอาสาสมัครจากวิกิพีเดีย (สำหรับผู้จัดรูปแบบ)
โปรดคลิก "เลือกและจองการจัดรูปแบบบทความ" เพื่อดูบทความที่แปลแล้ว หากคุณตัดสินใจที่จะจัดรูปแบบบทความดังกล่าว
หรือตอบปฏิเสธการแปลเนื่องจากคุณภาพไม่เพียงพอ กด "ตกลง" เพื่อไปยังขั้นตอน "ส่งการจัดรูปแบบบทความ"
ซึ่งเป็นขั้นตอนการจัดรูปแบบบทความรือปฏิเสธบทความ อนึ่ง อาสาสมัครสามารถออกจากขั้นตอนนี้ได้ทุกเวลา
และเข้าถึงได้ใหม่ผ่านทาง "ส่งการจัดรูปแบบบทความ" ในหน้าหลัก

### สำหรับผู้ดำเนินโครงการ (ผู้จัดการดูแล)
คลิก "อัปโหลดบทความขึ้นวิกิพีเดีย" เพื่อนำบทความไปลงวิกิพีเดีย บทความที่นำไปลงวิกิพีเดียแล้วจะสามารถเรียกดูได้จาก
"ดูบทความที่อัปโหลดขึ้นวิกิพีเดียแล้ว" ที่อยู่ในหน้าหลัก นอกจากนี้
ผู้จัดการดูแลยังสามารถเรียกคืนบทความที่ถูกปฏิเสธให้กลับมาจัดรูปแบบใหม่ได้ผ่าน "จัดการบทความที่ไม่ผ่านเกณฑ์" ในหน้าหลัก
''', 'markdown'),

    'letstranslate-back-to-home': u'กลับสู่หน้าหลัก',
    'letstranslate-no-item': u'ไม่มีรายการ',

    'letstranslate-index-for-translator': u'สำหรับผู้แปล',
    'letstranslate-index-for-formatter': u'สำหรับผู้จัดรูปแบบ',
    'letstranslate-index-for-organizer': u'สำหรับผู้จัดการดูแล',

    'letstranslate-index-translate': u'ส่งการแปลบทความ',
    'letstranslate-index-format_reserve': u'เลือกและจองการจัดรูปแบบบทความ',
    'letstranslate-index-format_submit': u'ส่งการจัดรูปแบบบทความ',
    'letstranslate-index-organize_submit': u'อัปโหลดบทความขึ้นวิกิพีเดีย',
    'letstranslate-index-organize_rejected': u'จัดการบทความที่ไม่ผ่านเกณฑ์',
    'letstranslate-index-organize_done': u'ดูบทความที่อัปโหลดขึ้นวิกิพีเดียแล้ว',

    'letstranslate-table-id': u'หมายเลขรายการ',
    'letstranslate-table-date': u'วันที่ส่ง',
    'letstranslate-table-name': u'ชื่อผู้ร่วมแปล',
    'letstranslate-table-site': u'ไซต์',
    'letstranslate-table-title': u'ชื่อหน้า',
    'letstranslate-row-view': u'ดู',

    'letstranslate-save-success': u'ส่งเรียบร้อย',
    'letstranslate-reject-success': u'ปฏิเสธบทความเรียบร้อย',
    'letstranslate-recover-success': u'กู้บทความเรียบร้อย',

    'letstranslate-pid-label': u'หมายเลขอ้างอิงของผู้แปล',
    'letstranslate-pid-placeholder': u'เช่น 123',
    'letstranslate-pid-tooltip': u'โปรดใส่หมายเลขอ้างอิงของคุณ',
    'letstranslate-email-label': u'อีเมล',
    'letstranslate-email-placeholder': u'เช่น username@dtac.co.th',
    'letstranslate-email-tooltip': u'โปรดใส่อีเมลที่สามารถติดต่อไปได้หากบทความที่แปลมาต้องแก้ไขเพิ่มเติม โปรดระวังว่าถึงแม้จะไม่มีการแสดงผลชื่ออีเมลนี้ในวิกิพีเดีย แต่ในเครื่องมือนี้ชื่ออีเมลจะปรากฎต่อสาธารณะ',
    'letstranslate-lang-label': u'ภาษาของบทความ',
    'letstranslate-lang-placeholder': u'เช่น en',
    'letstranslate-lang-tooltip': u'โปรดใส่ชื่อภาษาของบทความที่แปลมา',
    'letstranslate-fam-label': u'โครงการของบทความ',
    'letstranslate-fam-placeholder': u'เช่น wikipedia',
    'letstranslate-fam-tooltip': u'โปรดใส่ชื่อโครงการของบทความที่แปลมา',
    'letstranslate-title_translated-label': u'ชื่อบทความ (แปล)',
    'letstranslate-title_translated-placeholder': u'เช่น ขั้นตอนวิธี',
    'letstranslate-title_translated-tooltip': u'โปรดใส่ชื่อบทความที่แปลแล้ว',
    'letstranslate-title_untranslated-label': u'ชื่อบทความ (ดั้งเดิม)',
    'letstranslate-title_untranslated-placeholder': u'เช่น algorithm',
    'letstranslate-title_untranslated-tooltip': u'ชื่อบทความที่ยังไม่ได้แปล',
    'letstranslate-user_formatter-label': u'ชื่อของผู้จัดรูปแบบบทความ',
    'letstranslate-user_translator-label': u'ชื่อของผู้แปลที่จะให้แสดงในวิกิพีเดีย',
    'letstranslate-user_translator-placeholder': u'เช่น nattawan_s หรือ สมชาย สุขี',
    'letstranslate-user_translator-tooltip': u'''โปรดใส่ชื่อของผู้แปลที่จะให้แสดงในวิกิพีเดีย อาจเป็นชื่อจริง หรือชื่อเล่น หรือนามแฝงก็ได้
                                                 โปรดกาเครื่องหมายถูกหากชื่อที่กรอกเป็นชื่อบัญชีผู้ใช้ในวิกิพีเดีย''',
    'letstranslate-content_translated-label': u'เนื้อหาที่แปลแล้ว',
    'letstranslate-content_translated-placeholder': u'เช่น ขั้นตอนวิธี หรือ อัลกอริทึม (อังกฤษ: algorithm) '
                                                    u'หมายถึงกระบวนการแก้ปัญหาที่สามารถเข้าใจได้ ...',
    'letstranslate-content_translated-tooltip': u'โปรดใส่เนื้อหาบทความที่แปลแล้ว',
    'letstranslate-content_formatted-label': u'เนื้อหาที่จัดรูปแบบแล้ว',
    'letstranslate-content_formatted-placeholder': u"เช่น '''ขั้นตอนวิธี''' หรือ '''อัลกอริทึม''' {{lang-en|algorithm}} "
                                                   u"หมายถึงกระบวนการแก้[[ปัญหา]]ที่สามารถเข้าใจได้ ...",
    'letstranslate-content_formatted-tooltip': u'โปรดใส่เนื้อหาบทความที่จัดรูปแบบแล้ว',
    'letstranslate-length-label': u'ความยาวของเนื้อหาที่ยังไม่ได้จัดรูปแบบ',
    'letstranslate-length-word': u'คำ',
    'letstranslate-id-label': u'ลำดับที่',
    'letstranslate-summary-label': u'',
    'letstranslate-button-submit': u'ตกลง',
    'letstranslate-button-reject': u'ปฏิเสธการแปลนี้',
    'letstranslate-button-recover': u'กู้เพื่อให้จัดรูปแบบอีกรอบ',
    'letstranslate-confirm-text': u'''คุณได้ส่งบทความแปลความเรียบร้อยแล้ว คุณสามารถเริ่มแปลบทความใหม่ได้เลย
                                      อนึ่ง หากบทความนี้มีปัญหา จะมีผู้ใช้ติดต่อไปหาคุณผ่านทางอีเมล''',

    'letstranslate-summary': u'บทความนี้ แปลโดย {0} และได้รับการจัดรูปแบบวิกิโดย {1} ผ่านทางเครื่องมือแปลกันเถอะ!',
    'letstranslate-summary-label': u'คำอธิบายอย่างย่อในการสร้างหน้า',

    'permission-letstranslate': u'ผู้ใช้เครื่องมือแปลกันเถอะ!',
    'permission-letstranslate-description': u'กลุ่มที่สามารถเข้าถึงส่วน "สำหรับผู้จัดการดูแล" ในเครื่องมือแปลกันเถอะ!',
}

messages['en'] = {
}
