from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from crud.key_crud import create_key, delete_key, get_all_keys, get_key_by_id

router = APIRouter(prefix="/keys", tags=["Keys"])

@router.post("/")
def add_key(key_data: dict, db: Session = Depends(get_db)):
    return create_key(db, key_data)

@router.delete("/{key_id}")
def remove_key(key_id: int, db: Session = Depends(get_db)):
    if delete_key(db, key_id):
        return {"message": "Key deleted"}
    raise HTTPException(status_code=404, detail="Key not found")

@router.get("/")
def list_keys(db: Session = Depends(get_db)):
    return get_all_keys(db)

@router.get("/{key_id}")
def fetch_key(key_id: int, db: Session = Depends(get_db)):
    key = get_key_by_id(db, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    return key
