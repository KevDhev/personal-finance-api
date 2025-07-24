from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.auth.schemas import UserCreate, Token
from app.schemas.user import UserOut
from app.auth.crud import create_user, authenticate_user
from app.auth.dependencies import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app import crud

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_data: UserCreate, db: Session=Depends(get_db)):
    """
    Registra un nuevo usuario.
    
    - **username**: 3-50 caracteres (único)
    - **email**: Formato válido (único)
    - **password**: Mínimo 8 caracteres, 1 número y 1 símbolo
    """

    # Verifica si el usuario ya existe
    db_user = crud.get_user_by_username(db, username=user_data.username)

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Crea el usuario (la contraseña se hashea en crud.create_user)
    created_user = create_user(db=db, user_data=user_data)

    return created_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm=Depends(),
    db: Session=Depends(get_db)
):
    """
    Inicia sesión y devuelve un token JWT.
    
    - **username**: Tu nombre de usuario
    - **password**: Tu contraseña
    """

    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Crea token de acceso (expira en 30 mins por defecto)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}