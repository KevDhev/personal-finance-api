from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.schemas.movement import MovementOut

# Esquema base común (evita repetir campos)
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["KevDhev"])
    email: EmailStr = Field(..., examples=["kevdhev@example.com"])

# Esquema para creación (hereda de UserBase)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, examples=["qwerty123"])

# Esquema para actualización (todos los campos opcionales)
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

# Esquema para respuesta (sin contraseña)
class UserOut(UserBase):
    id: int
    created_at: datetime
    movements: List[MovementOut] = []   # Relación con movimientos

    class Config:
        from_attributes = True          # Habilita la compatibilidad con ORM
