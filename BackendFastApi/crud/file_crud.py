from sqlalchemy.orm import Session
from models.file_model import File
from models.file_model import FileCreate

def create_file(db: Session, file_data: FileCreate):
    file_obj = File(**file_data.dict())
    db.add(file_obj)
    db.commit()
    db.refresh(file_obj)
    return file_obj

def get_all_files(db: Session):
    return db.query(File).all()

def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.file_id == file_id).first()

def delete_file(db: Session, file_id: int):
    file_obj = db.query(File).filter(File.file_id == file_id).first()
    if file_obj:
        db.delete(file_obj)
        db.commit()
        return True
    return False
