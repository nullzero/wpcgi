#!/data/project/nullzerobot/python/bin/python
# -*- coding: utf-8 -*-

from wpcgi.db import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True, unique=True)
    date_touched = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def in_group(self, groups):
        return any(
            any(group == row.group for row in self.groups) for group in groups
        )

class UserGroup(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group = db.Column(db.String(255), primary_key=True)

    user = db.relationship("User", backref="groups")