# SI-Proiect/BackendFastApi/app/main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session
from .init_db import create_tables
# Modificăm importurile pentru a include noul router
from router import algorithm_router, file_router, key_router, performance_router, crypto_router

app = FastAPI()

create_tables()

app.include_router(key_router.router)
app.include_router(algorithm_router.router)
app.include_router(file_router.router)
app.include_router(performance_router.router)
app.include_router(crypto_router.router) # Adăugăm noul router