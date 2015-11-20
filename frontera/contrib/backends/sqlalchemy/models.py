# -*- coding: utf-8 -*-
import datetime

from sqlalchemy.types import TypeDecorator
from sqlalchemy import Column, String, Integer, PickleType, SmallInteger, Float
from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()


class DatetimeTimestamp(TypeDecorator):

    impl = String  # To use milliseconds in mysql
    timestamp_format = '%Y%m%d%H%M%S%f'

    def process_bind_param(self, value, _):
        if isinstance(value, datetime.datetime):
            return value.strftime(self.timestamp_format)
        raise ValueError('Not valid datetime')

    def process_result_value(self, value, _):
        return datetime.datetime.strptime(value, self.timestamp_format)


class MetadataModel(DeclarativeBase):
    __tablename__ = 'metadata'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    url = Column(String(1024), nullable=False)
    fingerprint = Column(String(40), primary_key=True, nullable=False)
    depth = Column(Integer, nullable=False)
    created_at = Column(DatetimeTimestamp(20), nullable=False)
    status_code = Column(String(20))
    score = Column(Float)
    error = Column(String(20))
    meta = Column(PickleType())
    headers = Column(PickleType())
    cookies = Column(PickleType())
    method = Column(String(6))

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<Metadata:%s (%s)>' % (self.url, self.fingerprint)


class StateModel(DeclarativeBase):
    __tablename__ = 'states'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    fingerprint = Column(String(40), primary_key=True, nullable=False)
    state = Column(SmallInteger())

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<State:%s=%d>' % (self.fingerprint, self.state)


class QueueModel(DeclarativeBase):
    __tablename__ = 'queue'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    id = Column(Integer, primary_key=True)
    partition_id = Column(Integer, index=True)
    score = Column(Float, index=True)
    url = Column(String(1024), nullable=False)
    fingerprint = Column(String(40), nullable=False)
    host_crc32 = Column(Integer, nullable=False)
    meta = Column(PickleType())
    headers = Column(PickleType())
    cookies = Column(PickleType())
    method = Column(String(6))

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<Queue:%s (%d)>' % (self.url, self.id)