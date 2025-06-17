from fastapi import FastAPI
from app.routers import movement
from app.database import Base, engine

# Required for table creation 
from app.models.user import User
from app.models.movement import Movement

app = FastAPI(
    title="Personal Finance API",
    description="API para gestionar finanzas personales",
    version="1.0.0"
)

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)

app.include_router(movement.router)
