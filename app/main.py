from fastapi import FastAPI
from app.routers import movement
from app.database import Base, engine
from app.auth.router import router as auth_router

# Required for table creation 
from app.models.user import User # type: ignore
from app.models.movement import Movement # type: ignore

app = FastAPI(
    title="Personal Finance API",
    description="API para gestionar finanzas personales",
    version="1.0.0"
)

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth_router)
app.include_router(movement.router)