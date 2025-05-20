from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from schemas.file_schemas import FileCreate, FileResponse
from crud import file_crud

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/", response_model=FileResponse)
def add_file(file_data: FileCreate, db: Session = Depends(get_db)):
    return file_crud.create_file(db, file_data)

@router.get("/", response_model=list[FileResponse])
def list_files(db: Session = Depends(get_db)):
    return file_crud.get_all_files(db)

@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file_obj = file_crud.get_file_by_id(db, file_id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")
    return file_obj

@router.delete("/{file_id}")
def remove_file(file_id: int, db: Session = Depends(get_db)):
    if file_crud.delete_file(db, file_id):
        return {"message": "File deleted"}
    raise HTTPException(status_code=404, detail="File not found")
