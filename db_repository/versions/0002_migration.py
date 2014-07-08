from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
category_mover = Table('category_mover', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date_created', DateTime, nullable=False),
    Column('date_edited', DateTime, nullable=False),
    Column('fam', String(length=31), nullable=False),
    Column('lang', String(length=7), nullable=False),
    Column('cat_from', String(length=255), nullable=False),
    Column('cat_to', String(length=255), nullable=False),
    Column('user_id', Integer),
    Column('status', Integer, nullable=False),
    Column('note', String(length=300), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['category_mover'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['category_mover'].drop()
