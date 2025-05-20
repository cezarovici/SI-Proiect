from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean, Enum, Text, TIMESTAMP, func
from app.db import Base

class Performance(Base):
    __tablename__ = 'performance'

    performance_id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.file_id', ondelete="CASCADE", onupdate="CASCADE"))
    algorithm_id = Column(Integer, ForeignKey('algorithms.algorithm_id', ondelete="RESTRICT", onupdate="CASCADE"))
    key_id = Column(Integer, ForeignKey('keys.key_id', ondelete="RESTRICT", onupdate="CASCADE"))
    operation_type = Column(Enum('encrypt', 'decrypt'), nullable=False)
    execution_time_ms = Column(Float, nullable=False)
    memory_usage_mb = Column(Float, nullable=False)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
