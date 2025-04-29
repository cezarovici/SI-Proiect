from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Algorithm
from db import get_db

app = FastAPI()

@app.get("/algorithms/")
def get_algorithms(db: Session = Depends(get_db)):
    return db.query(Algorithm).all()

@app.post("/algorithms/")
def create_algorithm(name: str, type: str, parameters: str, db: Session = Depends(get_db)):
    algorithm = Algorithm(name=name, type=type, parameters=parameters)
    db.add(algorithm)
    db.commit()
    db.refresh(algorithm)
    return algorithm

@app.put("/algorithms/{algorithm_id}")
def update_algorithm(algorithm_id: int, name: str, db: Session = Depends(get_db)):
    algorithm = db.query(Algorithm).filter(Algorithm.algorithm_id == algorithm_id).first()
    if not algorithm:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    algorithm.name = name
    db.commit()
    db.refresh(algorithm)
    return algorithm

@app.delete("/algorithms/{algorithm_id}")
def delete_algorithm(algorithm_id: int, db: Session = Depends(get_db)):
    algorithm = db.query(Algorithm).filter(Algorithm.algorithm_id == algorithm_id).first()
    if not algorithm:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    db.delete(algorithm)
    db.commit()
    return {"message": "Algorithm deleted"}
