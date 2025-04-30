from sqlalchemy.orm import Session
from models.key_model import Key

def create_key(db: Session, key_data: dict):
    new_key = Key(**key_data)
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return new_key

def delete_key(db: Session, key_id: int):
    key = db.query(Key).filter(Key.key_id == key_id).first()
    if key:
        db.delete(key)
        db.commit()
        return True
    return False

def get_all_keys(db: Session):
    return db.query(Key).all()

def get_key_by_id(db: Session, key_id: int):
    return db.query(Key).filter(Key.key_id == key_id).first()
