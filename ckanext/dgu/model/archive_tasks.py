import uuid
from datetime import datetime

from sqlalchemy import Column, MetaData
from sqlalchemy import types
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base

import ckan.model as model
from ckan.lib.base import *

log = __import__('logging').getLogger(__name__)

Base = declarative_base()

def make_uuid():
    return unicode(uuid.uuid4())

metadata = MetaData()

class ArchiveTask(Base):
    """
    Contains the latest information for archive tasks where each
    entry (by resource_id/dataset_id) is the most recent result.
    """
    __tablename__ = 'archive_task'

    id = Column(types.UnicodeText, primary_key=True, default=make_uuid)
    dataset_id = Column(types.UnicodeText, nullable=False, index=True)
    resource_id = Column(types.UnicodeText, nullable=False, index=True)

    response = Column(types.UnicodeText)
    error = Column(types.UnicodeText)
    first_failure = Column(types.DateTime)
    last_success = Column(types.DateTime)
    url_redirected_to = Column(types.UnicodeText)

    reason = Column(types.UnicodeText)
    status = Column(types.UnicodeText)
    failure_count = Column(types.Integer, default=0)

    created   = Column(types.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def create(cls, entity):
        c = cls()
        c.response = entity.value
        # unpack the error json
        c.created = entity.last_updated
        return c

def init_tables(e):
    Base.metadata.create_all(e)