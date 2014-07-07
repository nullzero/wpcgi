'''
from database import asDict
from selfdb import SelfDatabase, must_be
from datetime import datetime
import wpcgi.error

class STATUS(object):
    QUEUE_WAIT = 0
    QUEUE_APPROVED = 1
    DONE_ALL = 2
    DONE_FAILED = 3
    DONE_REJECTED = 4

    QUEUE = [QUEUE_WAIT, QUEUE_APPROVED]
    DONE = [DONE_ALL, DONE_FAILED, DONE_REJECTED]

class CategoryMoverDatabase(SelfDatabase):
    def connect(self):
        super(CategoryMoverDatabase, self).connect()

    @asDict
    def getQueue(self):
        return self.session.query(self.CategoryMover).filter(
            self.CategoryMover.status.in_(STATUS.QUEUE)).all()

    @asDict
    def getArchive(self):
        return self.session.query(self.CategoryMover).filter(
            self.CategoryMover.status.in_(STATUS.DONE)).all()

    @must_be(credit='APPROVED')
    def approve(self, rid):
        data = self.session.query(self.CategoryMover).filter(
            self.CategoryMover.rid == rid,
            self.CategoryMover.status == STATUS.QUEUE_WAIT
        ).first()

        if not data:
            raise wpcgi.error.IDNotFoundError()

        data.status = STATUS.QUEUE_APPROVED
        self.session.commit()

    @must_be(credit='APPROVED')
    def reject(self, rid):
        data = self.session.query(self.CategoryMover).filter(
            self.CategoryMover.rid == rid,
            self.CategoryMover.status.in_(STATUS.QUEUE)
        ).first()

        if not data:
            raise wpcgi.error.IDNotFoundError()

        data.status = STATUS.DONE_REJECTED
        self.session.commit()

    def queueStatus(self):
        if self.credit() >= self.credit('APPROVED'):
            return STATUS.QUEUE_APPROVED
        else:
            return STATUS.QUEUE_WAIT

    @must_be(credit='USER')
    def new(self, **kwargs):
        data = self.CategoryMover(date=datetime.now(),
                                  user=self.user,
                                  status=self.queueStatus(),
                                  **kwargs)
        self.session.add(data)
        self.session.commit()
        return data.rid

    @must_be(credit='USER')
    def edit(self, rid, **kwargs):
        data = self.session.query(self.CategoryMover).filter(
            self.CategoryMover.rid == rid,
            self.CategoryMover.status.in_(STATUS.QUEUE)
        ).first()

        if not data:
            raise wpcgi.error.IDNotFoundError()

        data.status = self.queueStatus()
        data.date = datetime.now()
        data.user = self.user

        for key in kwargs:
            setattr(data, key, kwargs[key])

        self.session.commit()

    @asDict
    @must_be(credit='USER')
    def loadEdit(self, rid):
        data = self.session.query(self.CategoryMover).filter(
            self.CategoryMover.rid == rid,
            self.CategoryMover.status.in_(STATUS.QUEUE)
        ).first()

        if not data:
            raise wpcgi.error.IDNotFoundError()

        return data

    def done(self, rid, status):
        data = self.session.query(self.CategoryMover).filter(
            self.CategoryMover.rid == rid,
        ).first()

        data.status = status

if __name__ == "__main__":
    cm = CategoryMoverDatabase(drop=True)
    cm.connect('Nullzero')
    print cm.getQueue()
    cm.new('A', 'B', 'Change Category from A to B')
    print cm.getQueue()
    cm.disconnect()
'''

