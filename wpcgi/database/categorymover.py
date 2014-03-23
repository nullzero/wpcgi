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
    def connect(self, user):
        super(CategoryMoverDatabase, self).connect(user)
    
    def getQueue(self):
        output = []
        for row in self.session.query(self.CategoryMover).filter(self.CategoryMover.status.in_(STATUS.QUEUE)).all():
            if row.status == STATUS.QUEUE_APPROVED:
                row.disable_approve = 'disabled'
                row.is_approved = 'success'
            
            if self.credit() < self.credit('APPROVED'):
                row.disable_approve = 'disabled'
                row.disable_reject = 'disabled'
                
            output.append(row)
        return output
        
    def getArchive(self, page):
        output = []
        for row in self.session.query(self.CategoryMover).filter(self.CategoryMover.status.in_(STATUS.DONE)).all():
            if row.status == STATUS.QUEUE_APPROVED:
                row.disable_approve = 'disabled'
                row.is_approved = 'success'
            
            if self.credit() < self.credit('APPROVED'):
                row.disable_approve = 'disabled'
                row.disable_reject = 'disabled'
                
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
    
    def queueStatus(self):
        if self.credit() >= self.credit('APPROVED'):
            return STATUS.QUEUE_APPROVED
        else:
            return STATUS.QUEUE_WAIT

    @must_be(credit='USER')
    def new(self, **kwargs):
        self.session.add(self.CategoryMover(date=datetime.now(), user=self.user, status=self.queueStatus(), **kwargs))
        self.session.commit()
    
    @must_be(credit='USER')
    def edit(self, rid, **kwargs):
        data = self.session.query(self.CategoryMover).filter(self.CategoryMover.rid == rid,
                                                             self.CategoryMover.status.in_(STATUS.QUEUE)).first()
        if not data:
            raise NotImplementedError('no id')
        
        data.status = self.queueStatus()
        data.date = datetime.now()
        data.user = self.user
        for key in kwargs:
            setattr(data, key, kwargs[key])
        self.session.commit()
    
    @must_be(credit='USER')
    def loadEdit(self, rid):
        data = self.session.query(self.CategoryMover).filter(self.CategoryMover.rid == rid,
                                                             self.CategoryMover.status.in_(STATUS.QUEUE)).first()
        if not data:
            raise NotImplementedError('no id')
        return row2dict(data)

if __name__ == "__main__":
    cm = CategoryMoverDatabase(drop=True)
    cm.connect('Nullzero')
    print cm.getQueue()
    cm.new('A', 'B', 'Change Category from A to B')
    print cm.getQueue()
    cm.disconnect()