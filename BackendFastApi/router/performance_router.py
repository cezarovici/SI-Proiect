from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from crud import performance_crud

router = APIRouter(prefix="/performance", tags=["Performance"])

@router.post("/")
def create_perf(perf_data: dict, db: Session = Depends(get_db)):
    return performance_crud.create_performance(db, perf_data)

@router.get("/{performance_id}")
def read_perf(performance_id: int, db: Session = Depends(get_db)):
    perf = performance_crud.get_performance(db, performance_id)
    if not perf:
        raise HTTPException(status_code=404, detail="Performance not found")
    return perf

@router.get("/")
def read_all_perf(db: Session = Depends(get_db)):
    return performance_crud.get_all_performances(db)

@router.delete("/{performance_id}")
def delete_perf(performance_id: int, db: Session = Depends(get_db)):
    success = performance_crud.delete_performance(db, performance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Performance not found")
    return {"detail": "Deleted successfully"}
