from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from app.schemas.movement import MovementOut

# Common base schema (avoids repeating fields) 
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["KevDhev"])
    email: EmailStr = Field(..., examples=["kevdhev@example.com"])

# Schema for creation (inherits from UserBase)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, examples=["qwerty123"])

# Schema for update (all fields optional) 
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

# Schema for response (without password) 
class UserOut(UserBase):
    id: int
    created_at: datetime
    movements: List[MovementOut] = []   # Relationship with movements 

    class Config:
        from_attributes = True          # Enables ORM compatibility  