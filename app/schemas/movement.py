from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Enumerado para tipo de movimiento
class MovementType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

# Esquema base común
class MovementBase(BaseModel):
    amount: float = Field(..., gt=0, description="Positive amount of movement")
    type: MovementType = Field(..., description="Type of movement: income or expense")
    description: Optional[str] = Field(None, max_length=255)

# Esquema para creación (incluye user_id)
class MovementCreate(MovementBase):
    user_id: int = Field(..., description="Associated user ID")
    date: Optional[datetime] = None

# Esquema para actualización (campos opcionales)
class MovementUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[MovementType] = None
    description: Optional[str] = Field(None, max_length=255)

# Esquema para respuesta (incluye todos los campos)
class MovementOut(MovementBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True          # Habilita la compatibilidad con ORM