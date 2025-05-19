from sqlalchemy.orm import Session
from models.file_model import File
from schemas.file_schemas import FileCreate

def create_file(db: Session, file_data: FileCreate) -> File:
    file_obj = File(**file_data)
    db.add(file_obj)
    db.commit()
    db.refresh(file_obj)
    return file_obj

def get_all_files(db: Session) -> list[File]:
    return db.query(File).all()

def get_file_by_id(db: Session, file_id: int) -> File | None:
    return db.query(File).filter(File.file_id == file_id).first()

def delete_file(db: Session, file_id: int) -> bool:
    file_obj = db.query(File).filter(File.file_id == file_id).first()
    if not file_obj:
        return False
    db.delete(file_obj)
    db.commit()
    return True
