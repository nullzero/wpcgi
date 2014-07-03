#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

messages = {}

messages['th'] = {
    'letstranslate-title': u'แปลกันเถอะ!',
    'letstranslate-description-content': u'สำหรับพนักงาน DTAC โปรดคลิก "ส่งการแปลบทความ" และกรอกข้อมูลเกี่ยวกับบทความที่คุณแปล พร้อมทั้งการแปล',

    'letstranslate-back-to-home': u'กลับสู่หน้าหลัก',
    'letstranslate-no-item': u'ไม่มีรายการ',

    'letstranslate-index-for-translator': u'สำหรับผู้แปล',
    'letstranslate-index-for-formatter': u'สำหรับผู้จัดรูปแบบ',
    'letstranslate-index-for-organizer': u'สำหรับผู้จัดการดูแล',

    'letstranslate-index-new': u'ส่งการแปลบทความ',
    'letstranslate-index-translated': u'เลือกและจองการจัดรูปแบบบทความ',
    'letstranslate-index-reserved': u'ส่งการจัดรูปแบบบทความ',
    'letstranslate-index-final': u'อัปโหลดบทความขึ้นวิกิพีเดีย',
    'letstranslate-index-rejected': u'จัดการบทความที่ไม่ผ่านเกณฑ์',
    'letstranslate-index-done': u'ดูบทความที่อัปโหลดขึ้นวิกิพีเดียแล้ว',

    'letstranslate-table-id': u'หมายเลขรายการ',
    'letstranslate-table-date': u'วันที่ส่ง',
    'letstranslate-table-name': u'ชื่อผู้ร่วมแปล',
    'letstranslate-table-title': u'ชื่อหน้า',
    'letstranslate-row-view': u'ดู',

    'letstranslate-save-success': u'ส่งเรียบร้อย',
    'letstranslate-reject-success': u'ปฏิเสธบทความเรียบร้อย',
    'letstranslate-recover-success': u'กู้บทความเรียบร้อย',

    'letstranslate-pid-label': u'หมายเลขอ้างอิง',
    'letstranslate-pid-placeholder': u'เช่น 123',
    'letstranslate-pid-tooltip': u'โปรดใส่หมายเลขอ้างอิงของคุณ',
    'letstranslate-email-label': u'อีเมล',
    'letstranslate-email-placeholder': u'เช่น username@dtac.co.th',
    'letstranslate-email-tooltip': u'โปรดใส่อีเมลที่สามารถติดต่อไปได้หากบทความที่แปลมาต้องแก้ไขเพิ่มเติม โปรดระวังว่าถึงแม้จะไม่มีการแสดงผลชื่ออีเมลนี้ในวิกิพีเดีย แต่ในเครื่องมือนี้ชื่ออีเมลจะปรากฎต่อสาธารณะ',
    'letstranslate-lang-label': u'ภาษาของบทความที่แปล',
    'letstranslate-lang-placeholder': u'เช่น en',
    'letstranslate-lang-tooltip': u'โปรดใส่ชื่อภาษาของบทความที่แปลมา',
    'letstranslate-fam-label': u'โครงการของบทความที่แปล',
    'letstranslate-fam-placeholder': u'เช่น wikipedia',
    'letstranslate-fam-tooltip': u'โปรดใส่ชื่อโครงการของบทความที่แปลมา',
    'letstranslate-title-label': u'ชื่อบทความที่แปล (แปล)',
    'letstranslate-title-placeholder': u'เช่น ขั้นตอนวิธี',
    'letstranslate-title-tooltip': u'โปรดใส่ชื่อบทความที่แปลแล้ว',
    'letstranslate-ftitle-label': u'ชื่อบทความที่แปล (ดั้งเดิม)',
    'letstranslate-ftitle-placeholder': u'เช่น algorithm',
    'letstranslate-ftitle-tooltip': u'ชื่อบทความที่ยังไม่ได้แปล',
    'letstranslate-name-label': u'ชื่อของผู้แปลที่จะให้แสดงในวิกิพีเดีย',
    'letstranslate-name-placeholder': u'เช่น nattawan_s หรือ สมชาย สุขี',
    'letstranslate-name-tooltip': u'โปรดใส่ชื่อของผู้แปลที่จะให้แสดงในวิกิพีเดีย อาจเป็นชื่อจริง หรือชื่อเล่น หรือนามแฝงก็ได้ โปรดกาเครื่องหมายถูกหากชื่อที่กรอกเป็นชื่อบัญชีผู้ใช้ในวิกิพีเดีย',
    'letstranslate-name2-label': u'ชื่อของผู้จัดรูปแบบที่จะให้แสดงในวิกิพีเดีย',
    'letstranslate-name2-placeholder': u'เช่น nattawan_s หรือ สมชาย สุขี',
    'letstranslate-name2-tooltip': u'โปรดใส่ชื่อของผู้จัดรูปแบบที่จะให้แสดงในวิกิพีเดีย อาจเป็นชื่อจริง หรือชื่อเล่น หรือนามแฝงก็ได้ โปรดกาเครื่องหมายถูกหากชื่อที่กรอกเป็นชื่อบัญชีผู้ใช้ในวิกิพีเดีย',
    'letstranslate-content-label': u'เนื้อหาที่แปลแล้ว',
    'letstranslate-content-placeholder': u'เช่น ขั้นตอนวิธี หรือ อัลกอริทึม (อังกฤษ: algorithm) หมายถึงกระบวนการแก้ปัญหาที่สามารถเข้าใจได้ ...',
    'letstranslate-content-tooltip': u'โปรดใส่เนื้อหาบทความที่แปลแล้ว',
    'letstranslate-content2-label': u'เนื้อหาที่จัดรูปแบบแล้ว',
    'letstranslate-content2-placeholder': u"เช่น '''ขั้นตอนวิธี''' หรือ '''อัลกอริทึม''' {{lang-en|algorithm}} หมายถึงกระบวนการแก้[[ปัญหา]]ที่สามารถเข้าใจได้ ...",
    'letstranslate-content2-tooltip': u'โปรดใส่เนื้อหาบทความที่จัดรูปแบบแล้ว',
    'letstranslate-button-submit': u'ตกลง',
    'letstranslate-button-reject': u'ปฏิเสธการแปลนี้',
    'letstranslate-button-recover': u'กู้เพื่อให้จัดรูปแบบอีกรอบ',
}

messages['en'] = {
}
