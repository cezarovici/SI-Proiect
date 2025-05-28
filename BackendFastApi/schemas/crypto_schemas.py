from pydantic import BaseModel

class EncryptRequest(BaseModel):
    file_id: int
    implementation: str

class DecryptRequest(BaseModel):
    file_id: int
    implementation: str 

class DecryptRequest(BaseModel): 
    file_id: int
    implementation: str
