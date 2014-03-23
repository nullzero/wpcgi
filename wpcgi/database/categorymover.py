from selfdb import SelfDatabase, must_be
from datetime import datetime
from database import row2dict

class STATUS(object):
    QUEUE_WAIT = 0
    QUEUE_APPROVED = 1
    DONE_ALL = 2
    DONE_FAILED = 3
    DONE_REJECTED = 4

    QUEUE = [QUEUE_WAIT, QUEUE_APPROVED]
    DONE = [DONE_ALL, DONE_FAILED, DONE_REJECTED]

class CategoryMoverDatabase(SelfDatabase):
    def getQueue(self):
        output = []
        for row in self.session.query(self.CategoryMover).filter(self.CategoryMover.status.in_(STATUS.QUEUE)).all():
            if row.status == STATUS.QUEUE_APPROVED:
                row.disable_approve = 'disabled'
            output.append(row)
        return output

    @must_be(credit='APPROVED')
    def approve(self, rid):
        data = self.session.query(self.CategoryMover).filter(self.CategoryMover.rid == rid,
                                                             self.CategoryMover.status == STATUS.QUEUE_WAIT).first()

        if not data:
            raise NotImplementedError('no id')
        data.status = STATUS.QUEUE_APPROVED
        self.session.commit()

    @must_be(credit='APPROVED')
    def reject(self, rid):
        data = self.session.query(self.CategoryMover).filter(self.CategoryMover.rid == rid,
                                                             self.CategoryMover.status.in_(STATUS.QUEUE)).first()

        if not data:
            raise NotImplementedError('no id')
        data.status = STATUS.DONE_REJECTED
        self.session.commit()

    @must_be(credit='USER')
    def new(self, cat_from, cat_to, note):
        if self.credit() >= self.credit('APPROVED'):
            status = STATUS.QUEUE_APPROVED
        else:
            status = STATUS.QUEUE_WAIT

        self.session.add(self.CategoryMover(date=datetime.now(), cat_from=cat_from, cat_to=cat_to,
                                            user=self.user, status=status, note=note))
        self.session.commit()

if __name__ == "__main__":
    cm = CategoryMoverDatabase(drop=True)
    cm.connect('Nullzero')
    print cm.getQueue()
    cm.new('A', 'B', 'Change Category from A to B')
    print cm.getQueue()
    cm.disconnect()