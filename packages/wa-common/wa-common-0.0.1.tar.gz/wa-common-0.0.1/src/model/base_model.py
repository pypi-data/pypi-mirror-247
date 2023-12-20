from sqlalchemy import Column, DateTime, func


class BaseModel(object):
    created = Column(DateTime, nullable=False, default=func.now())
    modified = Column(DateTime, nullable=True, onupdate=func.now())
