#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from model import Template
from datetime import datetime
from wpcgi.db import db, asDict
from utils import TextEngine, trycommit
from messages import msg
from flask import abort, flash, url_for, redirect

class STATUS(object):
    TRANSLATED = 1
    RESERVED = 2
    FORMATTED = 3
    REJECTED = 4
    DONE = 5

class LetsTranslate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_edited = db.Column(db.DateTime)
    pid = db.Column(db.Integer)
    fam = db.Column(db.String(31), nullable=False)
    lang = db.Column(db.String(7), nullable=False)
    title_untranslated = db.Column(db.String(255), nullable=False)
    title_translated = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    user_translator = db.Column(db.String(255), nullable=False)
    user_formatter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, nullable=False, default=STATUS.TRANSLATED)
    content_translated = db.Column(db.Text, nullable=False)
    content_formatted = db.Column(db.Text, nullable=True)

    user_formatter = db.relationship("User", backref="letstranslates")

class IDNotFoundError(Exception):
    def next(self):
        flash(msg['error-id-not-found'], 'danger')
        return redirect(url_for('letstranslate.index'))

class Model(Template):
    def doinit(self, id=None, action=None, mode=None):
        statusMap = {
            ('translate', None): 0,
            ('translate', 'result'): STATUS.TRANSLATED,
            ('format', 'reserve'): STATUS.TRANSLATED,
            ('format', 'submit'): STATUS.RESERVED,
            ('organize', 'submit'): STATUS.FORMATTED,
            ('organize', 'rejected'): STATUS.REJECTED,
            ('organize', 'done'): STATUS.DONE,
            ('reject', 'formatter'): STATUS.RESERVED,
            ('reject', 'organizer'): STATUS.FORMATTED,
            ('recover', None): STATUS.REJECTED,
            ('all', None): 0,
        }
        if (action, mode) not in statusMap.keys():
            abort(404)
        if id:
            self.data = LetsTranslate.query.filter_by(id=id).first()
            if not self.data or statusMap[(action, mode)] != self.data.status:
                raise IDNotFoundError
        else:
            self.data = None

        self.list = LetsTranslate.query.all()
        self.id = id
        self.mode = mode
        self.action = action
        self.engine = TextEngine(markup=False)

    def dovalidate(self):
        return True

    def getList(self):
        query = self.list
        if self.action == 'format':
            if self.mode == 'reserve':
                fun = lambda x: x.status == STATUS.TRANSLATED
            else:
                query = self.user.letstranslates
                fun = lambda x: x.status == STATUS.RESERVED
        elif self.action == 'organize':
            if self.mode == 'submit':
                fun = lambda x: x.status == STATUS.FORMATTED
            elif self.mode == 'rejected':
                fun = lambda x: x.status == STATUS.REJECTED
            elif self.mode == 'done':
                fun = lambda x: x.status == STATUS.DONE
        elif self.action == 'all':
            fun = lambda x: x.status != STATUS.REJECTED

        self.results = filter(fun, query)

        if self.action == 'all':
            for res in self.results:
                res.length = self.engine.length(self.engine.remove(res.content_translated))[0]

    def renderEdit(self):
        if (self.action, self.mode) == ('translate', None):
            return

        if not (hasattr(self.form, 'request') and self.form.request):
            data = asDict(self.data)
            for key in data:
                if hasattr(self.form, key):
                    getattr(self.form, key).data = data[key]

        if (self.action, self.mode) == ('format', 'submit'):
            self.form.content_formatted.data = ''

        if (self.action, self.mode) == ('organize', 'submit'):
            self.form.summary.data = msg['letstranslate-summary'].format(data['user_translator'], self.data.user_formatter.username)

        if hasattr(self.form, 'length'):
            self.form.length.data = self.engine.length(self.engine.remove(self.data.content_translated))[0]

        if hasattr(self.form, 'user_formatter'):
            self.form.user_formatter.data = self.data.user_formatter.username

    def save(self):
        wikify = None
        basedata = dict(
            date_edited = datetime.now()
        )
        fieldlist = []

        if self.action == 'translate':
            fieldlist = ['pid', 'user_translator', 'lang', 'fam',
                         'title_untranslated', 'title_translated',
                         'content_translated', 'email']
            if self.form.wikiuser.data:
                wikify = 'user_translator'
        elif self.action == 'format':
            if self.mode == 'reserve':
                basedata['user_formatter_id'] = self.user.id
                basedata['status'] = STATUS.RESERVED
            else:
                fieldlist = ['title_translated', 'content_formatted']
                basedata['status'] = STATUS.FORMATTED
        elif self.action == 'organize':
            if self.mode == 'submit':
                fieldlist = ['title_translated', 'content_formatted']
                basedata['status'] = STATUS.DONE
            else:
                return self.data.id

        for field in fieldlist:
            basedata[field] = getattr(self.form, field).data

        if wikify:
            basedata[wikify] = u'[[User:{}]]'.format(basedata[wikify])

        if self.data:
            for key in basedata:
                setattr(self.data, key, basedata[key])
            trycommit(db)
            return self.data.id
        else:
            letstranslate = LetsTranslate(**basedata)
            db.session.add(letstranslate)
            trycommit(db)
            return letstranslate.id

    def reject(self):
        self.data.status = STATUS.REJECTED
        trycommit(db)


    def recover(self):
        self.data.status = STATUS.TRANSLATED
        trycommit(db)

    def wikifyUser(self, row, name, wikify=False):
        if name.startswith('[[User:') and name.endswith(']]'):
            name = name[len('[[User:'):-len(']]')]
            wikify = True

        if wikify:
            name = u'<a href="http://{lang}.{fam}.org/wiki/User:{name}">{name}</a>'.format(fam=row.fam,
                                                                                           lang=row.lang,
                                                                                           name=name)
        return name
