from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List

class EmailLoginRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        min_length=5,
        max_length=254,
        description="User's email address for login"
    )

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }

class UserOut(BaseModel):
    id: int = Field(..., description="Unique identifier of the user")
    email: EmailStr = Field(..., description="User's email address")
    is_admin: bool = Field(..., description="Indicates if the user has admin privileges")

    model_config = ConfigDict(
        from_attributes=True,
        schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "is_admin": False
            }
        }
    )

class TokenResponse(BaseModel):
    access_token: str = Field(..., repr=False, description="JWT access token")
    token_type: str = Field("bearer", description="Type of the token")

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class PaginatedUsers(BaseModel):
    total: int
    skip: int
    limit: int
    users: List[UserOut]

    class Config:
        schema_extra = {
            "example": {
                "total": 1,
                "skip": 0,
                "limit": 100,
                "users": [
                    {
                        "id": 1,
                        "email": "user@example.com",
                        "is_admin": False
                    }
                ]
            }
        }