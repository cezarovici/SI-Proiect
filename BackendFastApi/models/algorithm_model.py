from sqlalchemy import Column, Integer, String, Enum
from db import Base

class Algorithm(Base):
    __tablename__ = 'algorithms'
    
    algorithm_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    type = Column(Enum('symmetric', 'asymmetric'), nullable=False)
