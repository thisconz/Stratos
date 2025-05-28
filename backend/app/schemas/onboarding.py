from pydantic import BaseModel, constr, EmailStr
from typing import Optional

class MFASetupRequest(BaseModel):
    pass  # no payload needed to start setup, can be empty

class MFASetupResponse(BaseModel):
    otp_uri: str
    qr_code_base64: str

class BackupCodeRequest(BaseModel):
    pass  # no payload needed, generates fresh backup codes

class BackupCodeResponse(BaseModel):
    backup_codes: list[str]

class MFAVerifyRequest(BaseModel):
    token: str

class MFAVerifyResponse(BaseModel):
    verified: bool

class BackupCodeVerifyRequest(BaseModel):
    code: str

class BackupCodeVerifyResponse(BaseModel):
    verified: bool

class ProfileSetupRequest(BaseModel):
    display_name: Optional[constr(min_length=1, max_length=50)]
    email: Optional[EmailStr]
    bio: Optional[constr(max_length=300)]

class PlanSelectionRequest(BaseModel):
    plan_id: constr(min_length=1)