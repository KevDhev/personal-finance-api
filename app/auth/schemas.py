from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    """
    Schema for the JWT authentication response.
    Contains the access token and its type.
    """

    access_token: str=Field(..., examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."])
    token_type: str=Field(..., examples=["bearer"])

class TokenData(BaseModel):
    """
    Data encapsulated in the JWT.
    Used for validation in protected endpoints.
    """

    username: Optional[str]=Field(None, examples=["john_doe"])
    exp: Optional[datetime]=Field(None, examples=["2024-12-31T23:59:59Z"])

class UserAuth(BaseModel):
    # Base schema for authentication.

    username: str=Field(..., min_length=3, max_length=50, examples=["john_doe"])

class UserCreate(UserAuth):
    """
    Schema for user registration.
    Extends UserAuth by adding email and password.
    """

    email: EmailStr=Field(..., examples=["user@example.com"])
    password: str=Field(
        ...,
        min_length=8,
        examples=["Str0ngP@ss"],
        pattern=r"^[A-Za-z\d@$!%*#?&]{8,}$"  
    )

class UserLogin(UserAuth):
    # Schema for login.

    password: str=Field(..., examples=["Str0ngP@ss"])

class UserInDB(UserAuth):
    """
    Internal schema for users in the database.
    Should not be publicly exposed.
    """

    email: EmailStr
    hashed_password: str
    is_active: bool=Field(default=True)