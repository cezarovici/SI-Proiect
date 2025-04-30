from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from crud.algorithm_crud import create_algorithm, get_all_algorithms, get_algorithm_by_id, delete_algorithm

router = APIRouter(prefix="/algorithms", tags=["Algorithms"])

@router.post("/")
def add_algorithm(algorithm_data: dict, db: Session = Depends(get_db)):
    return create_algorithm(db, algorithm_data)

@router.get("/")
def list_algorithms(db: Session = Depends(get_db)):
    return get_all_algorithms(db)

@router.get("/{algorithm_id}")
def fetch_algorithm(algorithm_id: int, db: Session = Depends(get_db)):
    algorithm = get_algorithm_by_id(db, algorithm_id)
    if not algorithm:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    return algorithm

@router.delete("/{algorithm_id}")
def remove_algorithm(algorithm_id: int, db: Session = Depends(get_db)):
    if delete_algorithm(db, algorithm_id):
        return {"message": "Algorithm deleted"}
    raise HTTPException(status_code=404, detail="Algorithm not found")
