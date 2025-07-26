from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.models.user import User
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Annotated, Optional, Any
from pathlib import Path
from dotenv import load_dotenv
from os import getenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# Configuration
SECRET_KEY = str(getenv("SECRET_KEY", ""))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Schema for token data
class TokenData(BaseModel):
    username: Optional[str] = None

# OAuth2 flow configuration 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Function to create JWT tokens
def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency to get the current user
def get_current_user(
    token:Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        user = crud.get_user_by_username(db, username=username)

        if user is None:
            raise credentials_exception
        
        return user
    except JWTError:
        raise credentials_exception