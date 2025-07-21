from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    """
    Esquema para la respuesta de autenticación JWT.
    Contiene el token de acceso y su tipo.
    """

    access_token: str=Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str=Field(..., examples=["bearer"])

class TokenData(BaseModel):
    """
    Datos encapsulados en el JWT.
    Usado para validación en endpoints protegidos.
    """

    username: Optional[str]=Field(None, examples=["john_doe"])
    exp: Optional[datetime]=Field(None, examples=["2024-12-31T23:59:59Z"])

class UserAuth(BaseModel):
    #Esquema base para autenticación.

    username: str=Field(..., min_length=3, max_length=50, examples=["john_doe"])

class UserCreate(UserAuth):
    """
    Esquema para registro de usuarios.
    Extiende UserAuth añadiendo email y password.
    """

    email: EmailStr=Field(..., examples=["user@example.com"])
    password: str=Field(
        ...,
        min_length=8,
        examples=["Str0ngP@ss"],
        pattern=r"^[A-Za-z\d@$!%*#?&]{8,}$"  
    )

class UserLogin(UserAuth):
    # Esquema para inicio de sesión.

    password: str=Field(..., examples=["Str0ngP@ss"])

class UserInDB(UserAuth):
    """
    Esquema interno para usuarios en base de datos.
    No debe exponerse públicamente.
    """

    email: EmailStr
    hashed_password: str
    is_active: bool=Field(default=True)