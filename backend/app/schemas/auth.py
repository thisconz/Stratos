from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str]

class OAuthProvider(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    # add other providers as needed
