from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Algorithm
from db import get_db

app = FastAPI()

@app.get("/algorithms/")
def get_algorithms(db: Session = Depends(get_db)):
    return db.query(Algorithm).all()
