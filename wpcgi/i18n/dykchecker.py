#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

messages = {}

messages['th'] = {
    'dykchecker': u'DYKChecker',
    'dykchecker-title': u'เครื่องมือตรวจสอบบทความรู้ไหมว่า',
    'dykchecker-description': u'เครื่องมือตรวจสอบว่าบทความผ่านเกณฑ์ขั้นต่ำของ "บทความรู้ไหมว่า" หรือไม่',
    'dykchecker-description-content': (
u'''เครื่องมือนี้มีไว้เพื่อตรวจสอบบทความต่าง ๆ ที่ได้รับเสนอชื่อให้ขึ้นหน้าแรกของวิกิพีเดียในหัวข้อ "[บทความรู้ไหมว่า](https://th.wikipedia.org/wiki/วิกิพีเดีย:รู้ไหมว่า)"
ว่าผ่านเกณฑ์ขั้นเบื้องต้นหรือไม่

#### วิธีใช้

1. กรอกชื่อหน้าที่จะให้ตรวจสอบลงในช่อง "ชื่อหน้า"
2. หากมีการตั้งค่าพิเศษ เช่น ให้เครื่องมือตรวจรุ่นปัจจุบันเทียบกับรุ่นเก่าที่กำหนดให้
หรือให้เครื่องมือเปลี่ยนเกณฑ์ความยาวขั้นต่ำของบทความรู้ไหมว่า ก็สามารถกรอกช่องต่าง ๆ ให้เปลี่ยนค่าได้ อย่างไรก็ตาม
หากไม่มีการตั้งค่าพิเศษสามารถข้ามช่องเหล่านั้นได้เลย
3. กดปุ่ม "ตรวจสอบ"

#### ข้อบทพร่องที่ทราบแล้ว

1. เครื่องมือตัดข้อความผิดพลาดสำหรับลิงก์ไฟล์ที่ข้างในมีลิงก์ข้อความอยู่
''', 'markdown'),

    'dykchecker-page-not-found': u'ไม่พบหน้าดังกล่าว',

    'dykchecker-revision-info': u'ข้อมูลรุ่น',
    'dykchecker-revision-info-value': u'รุ่นล่าสุดคือรุ่น {0} ของหน้า {1} แก้ไขโดย {2} เมื่อ {3} (UTC)',

    'dykchecker-inlineref': u'อ้างอิง',
    'dykchecker-inlineref-value': u'มีอ้างอิงในบรรทัดทั้งหมดจำนวน {0} แห่ง',
    'dykchecker-inlineref-desc': u'ข้อความที่ใช้เสนอบทความรู้ไหมว่าต้องมีอ้างอิงในบรรทัดยืนยันอย่างน้อย 1 แหล่ง',

    'dykchecker-length': u'ความยาว',
    'dykchecker-length-value': u'รุ่นล่าสุดมีความยาว {0} อักขระ',
    'dykchecker-length-desc': u'บทความรู้ไหมว่าต้องมีความยาวของความเรียงอย่างต่ำ {0} อักขระ',

    'dykchecker-creation': u'สร้างบทความ',
    'dykchecker-creation-value': u'บทความนี้สร้างโดย {2} เมื่อ {1} ({3} วันที่แล้ว - รุ่น {0})',
    'dykchecker-creation-new-desc': u'บทความรู้ไหมว่าต้องสร้างภายใน {0} วัน (ยกเว้นมีการปรับปรุงอย่างมีนัยยะสำคัญ)',
    'dykchecker-creation-desc': u'',

    'dykchecker-old-revision': u'รุ่นเก่า',
    'dykchecker-old-revision-value': u'รุ่น {0} ซึ่งเป็นรุ่นเก่าเมื่อ {1} UTC ({2} วันที่แล้ว) '
                                     u'มีความยาว {3} อักขระ ขณะนี้มีเนื้อหาเพิ่มขึ้น {4} เท่า',
    'dykchecker-old-revision-desc': u'ความยาวความเรียงต้องเพิ่มขึ้นอย่างน้อย {0} เท่า ภายในเวลา {1} วัน '
                                    u'ยกเว้นเป็นบทความสร้างใหม่<br/>'
                                    u'หมายเหตุ: หากจำนวนเนื้อหาที่เพิ่มติดลบ หมายความว่ามีเนื้อหาน้อยกว่าเดิม',
    'dykchecker-old-revision-not-exist': u'ไม่พบรุ่นเก่าภายในเวลา {0} วัน',

    'dykchecker-summary': u'<b>สรุป</b>',
    'dykchecker-summary-fail': u'บทความนี้ไม่ผ่านเกณฑ์บทความรู้ไหมว่า',
    'dykchecker-summary-pass': u'บทความนี้ผ่านเกณฑ์บทความรู้ไหมว่า สามารถ'
                               u'<a style="color: blue" '
                               u'href="//th.wikipedia.org/wiki/วิกิพีเดีย:รู้ไหมว่า/หัวข้อที่ถูกเสนอ">'
                               u'ดำเนินการเสนอ</a>บทความได้',

    'dykchecker-title-label': u'ชื่อหน้า',
    'dykchecker-oldid-label': u'รุ่นเก่า',
    'dykchecker-minlen-label': u'ความยาวขั้นต่ำ',
    'dykchecker-ratio-label': u'อัตราการขยายบทความ',
    'dykchecker-maxday-label': u'จำนวนวันในการตรวจสอบ',

    'dykchecker-title-placeholder': u'เช่น A',
    'dykchecker-oldid-placeholder': u'เช่น 12345',
    'dykchecker-minlen-placeholder': u'เช่น 2000',
    'dykchecker-ratio-placeholder': u'เช่น 3',
    'dykchecker-maxday-placeholder': u'เช่น 14',

    'dykchecker-title-tooltip': u'ชื่อหน้าที่จะให้เครื่องมือตรวจสอบว่าผ่านบทความรู้ไหมว่าหรือไม่ (จำเป็นต้องกรอก)',
    'dykchecker-oldid-tooltip': u'หมายเลขรุ่นหน้าเก่าที่จะให้เทียบกับรุ่นปัจจุบัน หากไม่กรอกเครื่องมือจะหารุ่นเก่าให้โดยอัตโนมัติ',
    'dykchecker-minlen-tooltip': u'ความยาวขั้นต่ำของบทความรู้ไหมว่า หากไม่กรอกจะใช้ค่า 2000',
    'dykchecker-ratio-tooltip': u'อัตราการขยายของบทความ (เกณฑ์สำหรับบทความเก่าที่ได้รับการปรับปรุงใหม่จนมีขนาดเพิ่มขึ้นหลายเท่า) หากไม่กรอกจะใช้ค่า 3',
    'dykchecker-maxday-tooltip': u'จำนวนวันที่จะให้เครื่องมือตรวจสอบ (ใช้เทียบกับอายุของบทความ และใช้หารุ่นเก่าที่จะนำมาเปรียบเทียบ) หากไม่กรอกจะใช้ค่า 14',

    'dykchecker-minlen-suffix': u'อักขระ',
    'dykchecker-ratio-suffix': u'เท่า',
    'dykchecker-maxday-suffix': u'วัน',

    'dykchecker-button-submit': u'ตรวจสอบ',
    'dykchecker-button-open-page': u'เปิดหน้า',
}