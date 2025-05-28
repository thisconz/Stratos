from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

# ----- User Account -----
class User(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime

# ----- Profile Settings -----
class UserProfile(BaseModel):
    id: UUID
    user_id: UUID
    full_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    theme: Optional[str]  # 'light', 'dark', etc.
    language: Optional[str]
    created_at: datetime

# ----- Session -----
class Session(BaseModel):
    id: UUID
    user_id: UUID
    device_name: str
    user_agent: Optional[str]
    ip_address: Optional[str]
    is_current: bool = False
    created_at: datetime
    last_seen: datetime

# ----- Multi-Factor Auth (MFA) -----
class MFAConfig(BaseModel):
    id: UUID
    user_id: UUID
    method: str  # 'totp', 'sms', 'email'
    secret: Optional[str]  # for TOTP
    enabled: bool
    backup_codes: Optional[list[str]]
    created_at: datetime

class Config:
        orm_mode = True