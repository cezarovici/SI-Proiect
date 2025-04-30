from fastapi import FastAPI
from sqlalchemy.orm import Session
from init_db import create_tables
from router import algorithm_router, file_router, key_router

app = FastAPI()

<<<<<<< HEAD
@app.get("/algorithms/")
def get_algorithms(db: Session = Depends(get_db)):
    return db.query(Algorithm).all()
=======
create_tables()

app.include_router(key_router.router)
app.include_router(algorithm_router.router)
app.include_router(file_router.router)
>>>>>>> 31670fdbda6caecf2bdc01fe41b0c2be79bdbeda
