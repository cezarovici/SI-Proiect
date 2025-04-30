from sqlalchemy.orm import Session
from models.performance_model import Performance

def create_performance(db: Session, perf_data: dict):
    performance = Performance(**perf_data)
    db.add(performance)
    db.commit()
    db.refresh(performance)
    return performance

def get_performance(db: Session, performance_id: int):
    return db.query(Performance).filter(Performance.performance_id == performance_id).first()

def get_all_performances(db: Session):
    return db.query(Performance).all()

def delete_performance(db: Session, performance_id: int):
    performance = db.query(Performance).filter(Performance.performance_id == performance_id).first()
    if performance:
        db.delete(performance)
        db.commit()
        return True
    return False
