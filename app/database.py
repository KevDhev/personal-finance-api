from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Database URL.
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in .env")

# Engine: main connection to the database  
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)

# Session factory 
SessionLocal = sessionmaker(
    autocommit=False,           # Don't autocommit 
    autoflush=False,            # Don't autoflush 
    bind=engine                 # Use the previously created engine
)

# Base class for models 
Base = declarative_base()

# Session generator for FastAPI dependencies  
def get_db():
    db = SessionLocal()         # Create a new session 

    try:
        yield db                # Provide the session to the endpoint 
    finally:
        db.close()              # Close the session afterward 