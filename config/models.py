import datetime
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, ForeignKey, Index, Integer, String, BigInteger, DateTime, Date, Boolean, Float, SmallInteger, Text
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy(session_options={"autoflush": False})

PREFIX_DB = 'zulu_'


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class UpdateAt(db.Model):
    __abstract__ = True
    update_at = Column(DateTime, nullable=False,
                       default=datetime.datetime.now, onupdate=datetime.datetime.now)


class CreateAt(db.Model):
    __abstract__ = True
    create_at = Column(DateTime, nullable=False, default=datetime.datetime.now)


class Scrap(Base, CreateAt, UpdateAt):
    __tablename__ = PREFIX_DB + 'scrap'
    __table_args__ = (
        Index("idx_ep_pr", "episode", "program"),
        Index("idx_ep_cr", "episode", "create_at", unique=True),
    )

    episode = Column(Integer, nullable=False, default='0', server_default='0')
    program = Column(String(255), nullable=False)
    url_img = Column(Text, nullable=True)
    url_video = Column(Text, nullable=True)
    title = Column(String(255), nullable=False)