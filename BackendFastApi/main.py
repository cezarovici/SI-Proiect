from fastapi import FastAPI
from sqlalchemy.orm import Session
from init_db import create_tables
from router import algorithm_router, key_router

app = FastAPI()

create_tables()

app.include_router(key_router.router)
app.include_router(algorithm_router.router)
