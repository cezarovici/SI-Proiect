from sqlalchemy.orm import Session
from models.algorithm_model import Algorithm

def create_algorithm(db: Session, algorithm_data: dict):
    algorithm = Algorithm(**algorithm_data)
    db.add(algorithm)
    db.commit()
    db.refresh(algorithm)
    return algorithm

def get_all_algorithms(db: Session):
    return db.query(Algorithm).all()

def get_algorithm_by_id(db: Session, algorithm_id: int):
    return db.query(Algorithm).filter(Algorithm.algorithm_id == algorithm_id).first()

def delete_algorithm(db: Session, algorithm_id: int):
    algorithm = db.query(Algorithm).filter(Algorithm.algorithm_id == algorithm_id).first()
    if algorithm:
        db.delete(algorithm)
        db.commit()
        return True
    return False
