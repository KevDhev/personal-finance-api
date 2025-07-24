from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Enum for movement type 
class MovementType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

# Common base schema 
class MovementBase(BaseModel):
    amount: float = Field(..., gt=0, description="Positive amount of movement")
    type: MovementType = Field(..., description="Type of movement: income or expense")
    description: Optional[str] = Field(None, max_length=255)

# Schema for creation 
class MovementCreate(MovementBase):
    date: Optional[datetime] = None

# Schema for update (optional fields)
class MovementUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[MovementType] = None
    description: Optional[str] = Field(None, max_length=255)

# Schema for response (includes all fields) 
class MovementOut(MovementBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True          # Enables ORM compatibility  