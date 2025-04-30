from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileCreate(BaseModel):
    original_path: str
    encrypted_path: str
    original_hash: Optional[str]
    encrypted_hash: Optional[str]
    algorithm_id: int
    key_id: int

class FileResponse(FileCreate):
    file_id: int
    encryption_date: datetime
    last_access: Optional[datetime]

    class Config:
        orm_mode = True
