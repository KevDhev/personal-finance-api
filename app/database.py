from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'

# Motor: conexión principal con la DB.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,           # No guardar automáticamente.
    autoflush=False,            # No enviar comandos hasta indicarlo.
    bind=engine                 # Usa el motor creado previamente.
)

# Clase base para modelos
Base = declarative_base()

# Generador de sesiones para dependencias de FastAPI
def get_db():
    db = SessionLocal()         # Crea una sesión nueva.

    try:
        yield db                # Entrega la sesión al endpoint.
    finally:
        db.close()              # Cierra la sesión después.