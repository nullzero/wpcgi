from sqlalchemy.engine.url import URL
from sqlalchemy import Column, Integer, DateTime, String, Table, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

url = URL(drivername='mysql', host='localhost', database='test',
          username='root', password='password')

engine = create_engine(name_or_url=url, convert_unicode=True)
metadata = MetaData(bind=engine)

class Row(Base):
    __table__ = Table('category_mover', metadata,
        Column('rid', Integer, primary_key=True),
        Column('date', DateTime, nullable=False),
        Column('cat_from', String(300), nullable=False),
        Column('cat_to', String(300), nullable=False),
        Column('user', String(300), nullable=False),
        Column('status', String(10), nullable=False)
    )

metadata.create_all()