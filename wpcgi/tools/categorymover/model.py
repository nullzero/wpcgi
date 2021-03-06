#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from model import Template
from wpcgi.db import db, asDict
from datetime import datetime
from flask import abort, url_for, redirect, flash
from messages import msg
from utils import trycommit

class STATUS(object):
    QUEUE_WAIT = 0
    QUEUE_APPROVED = 1
    DONE_ALL = 2
    DONE_FAILED = 3
    DONE_REJECTED = 4

    QUEUE = [QUEUE_WAIT, QUEUE_APPROVED]
    DONE = [DONE_ALL, DONE_FAILED, DONE_REJECTED]

color = {
    STATUS.DONE_ALL: 'success',
    STATUS.DONE_FAILED: 'warning',
    STATUS.DONE_REJECTED: 'danger',
    STATUS.QUEUE_APPROVED: 'success',
    STATUS.QUEUE_WAIT: '',
}

class CategoryMover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_edited = db.Column(db.DateTime, nullable=False)
    fam = db.Column(db.String(31), nullable=False)
    lang = db.Column(db.String(7), nullable=False)
    cat_from = db.Column(db.String(255), nullable=False)
    cat_to = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(300))

    user = db.relationship("User", backref="categorymovers")

class IDNotFoundError(Exception):
    def next(self):
        flash(msg['error-id-not-found'], 'danger')
        return redirect(url_for('categorymover.index'))

class Model(Template):
    def doinit(self, rid=None):
        if rid:
            self.data = CategoryMover.query.filter_by(id=rid).first()
            if not self.data:
                raise IDNotFoundError
        else:
            self.data = None

        self.queue = self.getByStatus(STATUS.QUEUE)
        self.num_queue = len(self.queue)
        self.nav_active = {'queue': '', 'new': '', 'archive': ''}
        self.rid = rid

    def getByStatus(self, status):
        if isinstance(status, list):
            return CategoryMover.query.filter(
                CategoryMover.status.in_(status)
            ).all()
        else:
            return CategoryMover.query.filter_by(status=status).all()

    def setActive(self, page=None):
        for key in self.nav_active:
            self.nav_active[key] = ''
        if page in self.nav_active:
            self.nav_active[page] = 'active'

    def getQueue(self):
        self.setActive('queue')
        self.results = self.queue
        for row in self.results:
          row.color = color[row.status]

          if not self.user.in_group(['categorymover', 'approved']):
              row.disable_approve = 'disabled'
              row.disable_reject = 'disabled'

          if row.status == STATUS.QUEUE_APPROVED:
              row.disable_approve = 'disabled'

    def getArchive(self):
        self.setActive('archive')
        self.results = self.getByStatus(STATUS.DONE)
        for row in self.results:
            row.color = color[row.status]

    def dovalidate(self):
        return True

    def save(self):
        basedata = dict(
            fam = self.form.fam.data,
            lang = self.form.lang.data,
            cat_from = self.form.cat_from.data,
            cat_to = self.form.cat_to.data,
            note = self.form.note.data,
            date_edited = datetime.now(),
            user_id = self.user.id
        )
        if self.user.in_group(['categorymover', 'approved']):
            basedata['status'] = STATUS.QUEUE_APPROVED
        else:
            basedata['status'] = STATUS.QUEUE_WAIT

        if self.data:
            for key in basedata:
                setattr(self.data, key, basedata[key])
            trycommit(db)
            return self.data.id
        else:
            categorymover = CategoryMover(**basedata)
            db.session.add(categorymover)
            trycommit(db)
            return categorymover.id

    def renderEdit(self):
        if self.rid:
            self.setActive('edit')

            if not self.form.request:
                data = asDict(self.data)
                for key in data:
                    if hasattr(self.form, key):
                        getattr(self.form, key).data = data[key]
        else:
            self.setActive('new')

    def changeStatus(self, mode):
        if self.data.status not in STATUS.QUEUE:
            raise IDNotFoundError
        if mode == 'reject':
            self.data.status = STATUS.DONE_REJECTED
        elif mode == 'approve':
            self.data.status = STATUS.QUEUE_APPROVED
        else:
            abort(404)
        trycommit(db)