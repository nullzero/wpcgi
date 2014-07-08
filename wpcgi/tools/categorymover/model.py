#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from model import Template
from wpcgi.db import db, asDict
from mwoauth import mwoauth
from datetime import datetime
import wpcgi.errors

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
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_edited = db.Column(db.DateTime, nullable=False)
    fam = db.Column(db.String(31), nullable=False)
    lang = db.Column(db.String(7), nullable=False)
    cat_from = db.Column(db.String(255), nullable=False)
    cat_to = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(300))

    user = db.relationship("User", backref="categorymovers")

    def __init__(self, *args, **kwargs):
        if not kwargs.get('user_id', None):
            kwargs['user_id'] = mwoauth.getUser().id
        super(CategoryMover, self).__init__(*args, **kwargs)

class Model(Template):
    def doinit(self, rid=None):
        print rid
        if rid:
            self.data = CategoryMover.query.filter_by(id=rid).first()
            print 'asd'
        else:
            print 'ghi'
            self.data = None

        self.queue = self.getByStatus(STATUS.QUEUE)
        self.num_queue = len(self.queue)
        self.nav_active = {'queue': '', 'new': '', 'archive': ''}
        self.rid = rid
        self.user = mwoauth.getUser()

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
        )
        if self.user.in_group(['categorymover', 'approved']):
            basedata['status'] = STATUS.QUEUE_APPROVED
        else:
            basedata['status'] = STATUS.QUEUE_WAIT

        if self.rid:
            for key in basedata:
                setattr(self.data, key, basedata[key])
            db.session.commit()
        else:
            categorymover = CategoryMover(**basedata)
            db.session.add(categorymover)
            db.session.commit()

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

    @mwoauth.in_group(['categorymover', 'approved'])
    def reject(self):
        if self.data.status not in STATUS.QUEUE:
            raise wpcgi.errors.IDNotFoundError()
        self.data.status = STATUS.DONE_REJECTED
        db.session.commit()

    @mwoauth.in_group(['categorymover', 'approved'])
    def approve(self):
        if self.data.status not in STATUS.QUEUE:
            raise wpcgi.errors.IDNotFoundError()
        self.data.status = STATUS.QUEUE_APPROVED
        db.session.commit()
