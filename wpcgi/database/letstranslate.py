from database import asDict
from selfdb import SelfDatabase, must_be
from datetime import datetime
import wpcgi.error

class STATUS(object):
    TRANSLATED = 1
    RESERVED = 2
    FINAL = 3

class LetsTranslateDatabase(SelfDatabase):
    def connect(self):
        super(LetsTranslateDatabase, self).connect()

    @asDict
    def getList(self):
        return self.session.query(self.LetsTranslate).all()

    def new(self, **kwargs):
        data = self.LetsTranslate(date=datetime.now(),
                                  status=STATUS.TRANSLATED,
                                  **kwargs)
        self.session.add(data)
        self.session.commit()

    def edit(self, rid, **kwargs):
        data = self.session.query(self.LetsTranslate).filter(
            self.LetsTranslate.rid == rid,
        ).first()

        if not data:
            raise wpcgi.error.IDNotFoundError()

        for key in kwargs:
            setattr(data, key, kwargs[key])

        self.session.commit()

    @asDict
    def loadEdit(self, rid):
        data = self.session.query(self.LetsTranslate).filter(
            self.LetsTranslate.rid == rid,
        ).first()

        if not data:
            raise wpcgi.error.IDNotFoundError()

        return data

    def done(self, rid, status):
        data = self.session.query(self.LetsTranslate).filter(
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
