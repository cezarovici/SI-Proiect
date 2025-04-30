from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Float, TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db import Base

class Algorithm(Base):
    __tablename__ = 'algorithms'
    
    algorithm_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    type = Column(Enum('symmetric', 'asymmetric'), nullable=False)


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
