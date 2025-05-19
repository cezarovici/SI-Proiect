from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer, String, func

from app.db import Base

class File(Base):
    __tablename__ = 'files'
    
    file_id = Column(Integer, primary_key=True, index=True)
    original_path = Column(String(255), nullable=False)
    encrypted_path = Column(String(255), nullable=False)
    original_hash = Column(String(64))
    encrypted_hash = Column(String(64))
    algorithm_id = Column(Integer, ForeignKey('algorithms.algorithm_id', ondelete="RESTRICT", onupdate="CASCADE"))
    key_id = Column(Integer, ForeignKey('keys.key_id', ondelete="RESTRICT", onupdate="CASCADE"))
    encryption_date = Column(TIMESTAMP, server_default=func.current_timestamp())
    last_access = Column(TIMESTAMP)