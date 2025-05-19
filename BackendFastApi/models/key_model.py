from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db import Base

class Key(Base):
    __tablename__ = 'keys'

    key_id = Column(Integer, primary_key=True, index=True)
    algorithm_id = Column(Integer, ForeignKey('algorithms.algorithm_id', ondelete="CASCADE", onupdate="CASCADE"))
    key_name = Column(String(100), nullable=False)
    key_value = Column(Text)
    public_key = Column(Text)
    private_key = Column(Text)
    creation_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    expiration_date = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)
