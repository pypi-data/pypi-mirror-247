from sqlalchemy import Column, String

from .base_model import BaseModel


class AuditedModel(BaseModel):
    c_owner = Column("c_owner", String(45), nullable=False)
    m_owner = Column("c_owner", String(45), nullable=True)
